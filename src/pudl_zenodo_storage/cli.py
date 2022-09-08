#!/usr/bin/env python
"""A script for archiving raw PUDL data on Zenodo."""

import argparse
import glob
import io
import json
import os
import sys
from hashlib import md5

import datapackage
import requests

import pudl_zenodo_storage as pzs
from pudl_zenodo_storage.zs.core import ZenodoStorage

ROOT_DIR = os.environ.get(
    "PUDL_IN", os.path.join(os.path.expanduser("~"), "Downloads", "pudl_scrapers")
)
ROOT_DIR = os.path.join(ROOT_DIR, "scraped")


def local_fileinfo(file_paths):
    """
    Produce a dict describing file names, paths, and md5 hashes.

    Args:
        file_paths (list): file path strings, as provided from the CLI.

    Returns:
        dict: of form {filename: {path: str, checksum: str (md5)}}

    """

    def file_md5s(file_path):
        hash_md5 = md5()  # nosec: B324

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)

        return hash_md5.hexdigest()

    metadata = {}

    for fp in file_paths:
        path, name = os.path.split(os.path.abspath(fp))
        checksum = file_md5s(fp)

        if name in metadata:
            raise ValueError(
                f"File names must be unique: {path} name conflicts "
                f"with {metadata[name]['path']}/{name}"
            )

        metadata[name] = {"path": path, "checksum": checksum}

    return metadata


def remote_fileinfo(zenodo, deposition):
    """
    Collect and shape file data from an existing Zenodo deposition.

    Args:
        zenodo: a zs.ZenodoStorage manager
        deposition: the deposition details, as retrieved from Zenodo

    Returns:
        dict: of form {filename: {path: str, checksum: str (md5)}}

    """
    url = deposition["links"]["files"]
    response = requests.get(url, params={"access_token": zenodo.key})

    if response.status_code > 299:
        msg = f"Unable to get files for {url}: {response}"
        raise RuntimeError(msg)

    try:
        jsr = response.json()
    except:  # noqa: E722
        msg = f"Invalid remote file data at {url}: {response}"
        raise ValueError(msg)

    files = jsr
    return {item["filename"]: item for item in files}


def new_datapackage(zenodo, datapackager, deposition):
    """
    Add a new datapackage.json file to the given deposition.

    Args:
        zenodo: a zs.ZenodoStorage manager
        datapackager: a data package generation function that takes a list of
            Zenodo file descriptors and produces the complete frictionless
            datapackage json.
            e.g. pzs.frictionless.eia860.datapackager
        deposition: the deposition details, as retrieved from Zenodo. Must be
                    in an editable state.

    Returns:
        None: Raises errors on failure.

    """
    files = remote_fileinfo(zenodo, deposition)

    if "datapackage.json" in files:
        requests.delete(
            files["datapackage.json"]["links"]["self"],
            params={"access_token": zenodo.key},
        )
        files.pop("datapackage.json")

    datapkg_descriptor = datapackager(files.values())
    datapkg_json = json.dumps(datapkg_descriptor, indent=4, sort_keys=True)
    datapkg = datapackage.Package(datapkg_descriptor)
    if not datapkg.valid:
        zenodo.logger.error(
            f"Found the following {len(datapkg.errors)} datapackage validation errors:"
        )
        for e in datapkg.errors:
            print(f"  * {e}")
        raise datapkg.errors[0]
    fcontents = io.BytesIO(bytes(datapkg_json, encoding="utf-8"))
    zenodo.upload(deposition, "datapackage.json", fcontents)


def action_steps(new_files, old_files):
    """
    Determine which files need to be created, updated, and deleted.

    Args:
        new_files (dict): local files, per local_fileinfo(...)
        old_files (dict): previous files, per remote_fileinfo(...)

    Returns:
        dict: containing:
        {create: {<fileinfo>}, update: {<fileinfo>}, delete: {<fileinfo>}}

    """
    actions = {"create": {}, "update": {}, "delete": {}}

    for filename, data in new_files.items():

        if filename == "datapackage.json":
            continue

        if filename not in old_files:
            actions["create"][filename] = data
        elif data["checksum"] != old_files[filename]["checksum"]:
            actions["update"][filename] = old_files[filename]
            actions["update"][filename]["path"] = data["path"]

    for filename, data in old_files.items():

        if filename == "datapackage.json":
            continue

        if filename not in new_files:
            actions["delete"][filename] = data

    return actions


def execute_actions(zenodo, deposition, datapackager, steps):
    """
    Execute all actions from the given steps.

    Args:
        zenodo: a zs.ZenodoStorage manager
        deposition: deposition descriptor as retrieved from Zenodo.
        datapackager: a data package generation function that takes a list of
            Zenodo file descriptors and produces the complete frictionless
            datapackage json.
            e.g. pzs.frictionless.eia860.datapackager
        steps: dict of file info to create, update, and delete, per
            action_steps(...)

    Returns:
        New deposition data, per https://developers.zenodo.org/#depositions,
        or error on failure

    """
    if steps["create"] == {} and steps["update"] == {} and steps["delete"] == {}:

        zenodo.logger.info(f"No changes for deposition {deposition['title']}")
        return

    if deposition["submitted"]:
        new_deposition = zenodo.new_deposition_version(deposition["conceptdoi"])
    else:
        new_deposition = deposition

    nd_files = remote_fileinfo(zenodo, new_deposition)

    for filename, data in steps["create"].items():
        path = os.path.join(data["path"], filename)

        with open(path, "rb") as f:
            zenodo.upload(new_deposition, filename, f)
            zenodo.logger.info(f"Uploaded {path}")

    for filename, data in steps["update"].items():
        requests.delete(
            nd_files[filename]["links"]["self"], params={"access_token": zenodo.key}
        )

        path = os.path.join(data["path"], filename)

        with open(path, "rb") as f:
            zenodo.upload(new_deposition, filename, f)
            zenodo.logger.info(f"Replaced {path}")

    for filename, data in steps["delete"].items():
        requests.delete(
            nd_files[filename]["links"]["self"], params={"access_token": zenodo.key}
        )
        zenodo.logger.info(f"Deleted {filename}")

    # Replace the datapackage json
    new_datapackage(zenodo, datapackager, new_deposition)

    return new_deposition


def initial_run(zenodo, key_id, metadata, datapackager, file_paths):
    """
    Create the first version of a Zenodo archive.

    Args:
        zenodo: a zs.ZenodoStorage manager
        key_id: keyword uuid, such as pzs.zs.metadata.eia860_uuid
        metadata: the zenodo_store metadata (NOT frictionless datapackage data!)
            for the deposition, such as pzs.zs.metadata.eia860
        datapackager: a data package generation function that takes a list of
            Zenodo file descriptors and produces the complete frictionless
            datapackage json.
            e.g. pzs.frictionless.eia860.datapackager
        file_paths: a list of files to upload

    Returns:
        Deposition data per https://developers.zenodo.org/#depositions,
        raises an error on failure

    """
    # Only run if the archive really has never been created

    if key_id not in metadata["keywords"]:
        # Not auto-correcting because it could mean a mixup between the
        # frictionless datapackage and the zenodo metadata
        raise ValueError("key_id missing from metadata keywords")

    try:
        deposition = zenodo.get_deposition(f'keyword="{key_id}"')
        exists = deposition is not None
    except RuntimeError:
        exists = False

    if exists:
        raise RuntimeError(
            f"Cannot initialize {metadata['title']}, it already exists at "
            f"{deposition['links']['html']}"
        )

    # New deposition
    deposition = zenodo.create_deposition(metadata)

    # Upload all requested files
    for fp in file_paths:
        path, name = os.path.split(fp)

        with open(fp, "rb") as f:
            zenodo.upload(deposition, name, f)
            zenodo.logger.info(f"Uploaded {fp}")

    # Save the datapackage.json
    new_datapackage(zenodo, datapackager, deposition)

    return deposition


def parse_main():
    """Process base commands from the CLI."""
    parser = argparse.ArgumentParser(description="Upload PUDL data archives to Zenodo")
    parser.add_argument(
        "--noop",
        action="store_true",
        default=False,
        help="Review changes without uploading",
    )
    parser.add_argument(
        "--sandbox",
        action="store_true",
        help="Use Zenodo sandbox server",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Print logging messages to stdout",
    )
    parser.add_argument(
        "--loglevel",
        help="Set log level",
        default="INFO",
    )
    parser.add_argument(
        "--initialize",
        action="store_true",
        help="Produce the first version of a new Zenodo deposition.",
    )
    parser.add_argument(
        "--files",
        nargs="*",
        help="Override default file list. By default, the most recent files "
        f"from {ROOT_DIR} will be uploaded.",
    )
    parser.add_argument(
        "deposition",
        help="Name of the Zenodo deposition. Supported: censusdp1tract, "
        "eia860, eia861, eia923, epacems, epacamd_eia, "
        "ferc1, ferc2, ferc714, eia860m",
    )
    return parser.parse_args()


def archive_selection(deposition_name):  # noqa: C901
    """
    Produce the datasets needed to run the archiver.

    Args:
        argument: str name for a deposition, as input from the cli.

    Returns:
        {
            key_id: a uuid string from pzs.zs.metadata,
            metadata: a metadata descriptor from pzs.zs.metadata
            datapackager: a datapackager from the appropriate frictionless
                          library
            latest_files: str path of the most recently scraped copy of the
                          archive
        }

    """

    def latest_files(name):
        sources = os.path.join(ROOT_DIR, name, "*")
        previous = sorted(glob.glob(sources))

        if previous == []:
            return []

        return glob.glob(os.path.join(previous[-1], "*"))

    if deposition_name == "censusdp1tract":
        return {
            "key_id": pzs.zs.metadata.censusdp1tract_uuid,
            "metadata": pzs.zs.metadata.censusdp1tract,
            "datapackager": pzs.frictionless.censusdp1tract.datapackager,
            "latest_files": latest_files("censusdp1tract"),
        }

    if deposition_name == "eia860":
        return {
            "key_id": pzs.zs.metadata.eia860_uuid,
            "metadata": pzs.zs.metadata.eia860,
            "datapackager": pzs.frictionless.eia860.datapackager,
            "latest_files": latest_files("eia860"),
        }

    if deposition_name == "eia860m":
        return {
            "key_id": pzs.zs.metadata.eia860m_uuid,
            "metadata": pzs.zs.metadata.eia860m,
            "datapackager": pzs.frictionless.eia860m.datapackager,
            "latest_files": latest_files("eia860m"),
        }

    if deposition_name == "eia861":
        return {
            "key_id": pzs.zs.metadata.eia861_uuid,
            "metadata": pzs.zs.metadata.eia861,
            "datapackager": pzs.frictionless.eia861.datapackager,
            "latest_files": latest_files("eia861"),
        }

    if deposition_name == "eia923":
        return {
            "key_id": pzs.zs.metadata.eia923_uuid,
            "metadata": pzs.zs.metadata.eia923,
            "datapackager": pzs.frictionless.eia923.datapackager,
            "latest_files": latest_files("eia923"),
        }

    if deposition_name == "epacems":
        return {
            "key_id": pzs.zs.metadata.epacems_uuid,
            "metadata": pzs.zs.metadata.epacems,
            "datapackager": pzs.frictionless.epacems.datapackager,
            "latest_files": latest_files("epacems"),
        }

    if deposition_name == "epacamd_eia":
        return {
            "key_id": pzs.zs.metadata.epacamd_eia_uuid,
            "metadata": pzs.zs.metadata.epacamd_eia,
            "datapackager": pzs.frictionless.epacamd_eia.datapackager,
            "latest_files": latest_files("epacamd_eia"),
        }

    if deposition_name == "ferc1":
        return {
            "key_id": pzs.zs.metadata.ferc1_uuid,
            "metadata": pzs.zs.metadata.ferc1,
            "datapackager": pzs.frictionless.ferc1.datapackager,
            "latest_files": latest_files("ferc1"),
        }

    if deposition_name == "ferc2":
        return {
            "key_id": pzs.zs.metadata.ferc2_uuid,
            "metadata": pzs.zs.metadata.ferc2,
            "datapackager": pzs.frictionless.ferc2.datapackager,
            "latest_files": latest_files("ferc2"),
        }

    if deposition_name == "ferc714":
        return {
            "key_id": pzs.zs.metadata.ferc714_uuid,
            "metadata": pzs.zs.metadata.ferc714,
            "datapackager": pzs.frictionless.ferc714.datapackager,
            "latest_files": latest_files("ferc714"),
        }

    raise ValueError(f"Unsupported archive: {deposition_name}")


def main():
    """A CLI for the PUDL Zenodo Storage system."""
    args = parse_main()

    if args.sandbox:
        zenodo_upload_token = os.environ["ZENODO_SANDBOX_TOKEN_UPLOAD"]
    else:
        zenodo_upload_token = os.environ["ZENODO_TOKEN_UPLOAD"]

    zenodo = ZenodoStorage(
        key=zenodo_upload_token,
        testing=args.sandbox,
        verbose=args.verbose,
        loglevel=args.loglevel,
    )

    sel = archive_selection(args.deposition)

    if getattr(args, "files", None) is None:
        files = sel["latest_files"]
    else:
        files = args.files

    files.sort()

    if args.initialize:
        if args.noop:
            for f in files:
                zenodo.logger.info(f"Archive would contain: {f}")
            sys.exit()

        result = initial_run(
            zenodo, sel["key_id"], sel["metadata"], sel["datapackager"], files
        )

        zenodo.logger.info(
            "Your new deposition archive is ready for review at "
            f"{result['links']['html']}"
        )
        sys.exit()

    local = local_fileinfo(files)

    deposition = zenodo.get_deposition(f"keywords: \"{sel['key_id']}\"")

    if deposition is None:
        raise ValueError("Deposition not found. You may need to --initialize")

    remote = remote_fileinfo(zenodo, deposition)
    steps = action_steps(local, remote)

    if args.noop:
        print(json.dumps(steps, indent=4, sort_keys=True))
        sys.exit()

    result = execute_actions(zenodo, deposition, sel["datapackager"], steps)

    if result is not None:
        zenodo.logger.info(
            "A new version of your deposition is ready for review "
            f"at {result['links']['html']}"
        )


if __name__ == "__main__":
    main()
