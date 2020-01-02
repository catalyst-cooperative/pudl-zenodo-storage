#!/usr/bin/env python
# -*- coding: utf-8

import argparse
import io
import json
from hashlib import md5
import os
import requests
import sys

import frictionless.eia860
from zs import ZenStorage
import zs.metadata


"""
zen_store.py --help
zen_store.py [--noop] [--test] eia860 ~/tmp/*.zip
"""


def local_fileinfo(file_paths):
    """
    Produce a dict describing file names, paths, and md5 hashes.

    Args:
        file_paths: a list file path strings, as provided from the CLI

    Returns:
        dict of form {filename: {path: str, checksum: str (md5)}}
    """
    def file_md5s(file_path):
        hash_md5 = md5()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)

        return hash_md5.hexdigest()

    metadata = {}

    for fp in file_paths:
        path, name = os.path.split(os.path.abspath(fp))
        checksum = file_md5s(fp)

        if name in metadata:
            msg = "File names must be unique: %s name conflicts with %s/%s" % (
                path, metadata[name]["path"], name)
            raise ValueError(msg)

        metadata[name] = {"path": path, "checksum": checksum}

    return metadata


def remote_fileinfo(zenodo, deposition):
    """
    Collect and shape file data from an existing Zenodo deposition

    Args:
        zenodo: a zs.ZenStorage manager
        deposition: the deposition details, as retrieved from Zenodo

    Returns:
        dict of form {filename: {path: str, checksum: str (md5)}}
    """
    response = requests.get(deposition["links"]["files"],
                            params={"access_token": zenodo.key})
    jsr = response.json()

    if response.status_code > 299:
        raise RuntimeError("Unable to get files: %s" % jsr)

    files = jsr
    return {item["filename"]: item for item in files}


def new_datapackage(zenodo, datapackager, deposition):
    """
    Add a new datapackage.json file to the given deposition

    Args:
        zenodo: a zs.ZenStorage manager
        datapackager: a data package generation function that takes a list of
            Zenodo file descriptors and produces the complete frictionless
            datapackage json.
            e.g. frictionless.eia860_archive.datapackager
        deposition: the deposition details, as retrieved from Zenodo. Must be
                    in an editable state.

    Returns:
        None. Raises errors on failure.
    """
    files = remote_fileinfo(zenodo, deposition)

    if "datapackage.json" in files:
        requests.delete(
            files["datapackage.json"]["links"]["self"],
            params={"access_token": zenodo.key})
        files.pop("datapackage.json")

    datapackage = json.dumps(datapackager(files.values()))
    fcontents = io.BytesIO(bytes(datapackage, encoding="utf-8"))
    zenodo.upload(deposition, "datapackage.json", fcontents)


def action_steps(new_files, old_files):
    """
    Determine which files need to be created, updated, and deleted

    Args:
        new_files: dict of local files, per local_fileinfo(...)
        old_files: dict of previous files, per remote_fileinfo(...)

    Returns:
        dict of:
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
        zenodo: a zs.ZenStorage manager
        deposition: deposition descriptor as retrieved from Zenodo.
        datapackager: a data package generation function that takes a list of
            Zenodo file descriptors and produces the complete frictionless
            datapackage json.
            e.g. frictionless.eia860_archive.datapackager
        steps: dict of file info to create, update, and delete, per
            action_steps(...)

    Return:
        None, or error on failure
    """
    if steps["create"] == {} and steps["update"] == {} and \
            steps["delete"] == {}:
        return

    new_deposition = zenodo.new_deposition_version(deposition["conceptdoi"])
    nd_files = remote_fileinfo(zenodo, new_deposition)

    for filename, data in steps["create"].items():
        path = os.path.join(data["path"], filename)

        with open(path, "rb") as f:
            zenodo.upload(new_deposition, filename, f)

    for filename, data in steps["update"].items():
        requests.delete(nd_files[filename]["links"]["self"],
                        params={"access_token": zenodo.key})

        path = os.path.join(data["path"], filename)

        with open(path, "rb") as f:
            zenodo.upload(new_deposition, filename, f)

    for filename, data in steps["delete"].items():
        requests.delete(nd_files[filename]["links"]["self"],
                        params={"access_token": zenodo.key})

    # Replace the datapackage json
    new_datapackage(zenodo, datapackager, new_deposition)
    zenodo.publish(new_deposition)


def initial_run(zenodo, metadata, datapackager, file_paths):
    """
    Create the first version of a Zenodo archive.

    Args:
        zenodo: a zs.ZenStorage manager
        metadata: the zen_store metadata (NOT frictionless datapackage data!) for
            the deposition, such as zen_store.metadata.eia860
        datapackager: a data package generation function that takes a list of
            Zenodo file descriptors and produces the complete frictionless
            datapackage json.
            e.g. frictionless.eia860_archive.datapackager
        file_paths: a list of files to upload

    Returns:
        None, raises an error on failure
    """
    # Only run if the archive really has never been created
    try:
        deposition = zenodo.get_deposition('title="%s"' % metadata["title"])
        exists = deposition is not None
    except RuntimeError as err:
        exists = False

    if exists:
        raise RuntimeError("Cannot initialize %s, it already exists" %
                           metadata["title"])

    # New deposition
    deposition = zenodo.create_deposition(metadata)

    # Upload all requested files
    for fp in file_paths:
        path, name = os.path.split(fp)

        with open(fp, "rb") as f:
            zenodo.upload(deposition, name, f)

    # Save the datapackage.json
    new_datapackage(zenodo, datapackager, deposition)

    # Publish
    zenodo.publish(deposition)


def parse_main():
    """
    Process base commands from the CLI
    """
    parser = argparse.ArgumentParser(
        description="Upload PUDL data archives to Zenodo")
    parser.add_argument("--noop", action="store_true", default=False,
                        help="Review changes without uploading")
    parser.add_argument("--sandbox", action="store_true",
                        help="Use Zenodo sandbox server")
    parser.add_argument(
        "--initialize", action="store_true",
        help="Produce the first version of a new Zenodo deposition.")
    parser.add_argument("deposition", help="Name of the Zenodo deposition."
                        " Supported: eia860_source")

    parser.add_argument("files", nargs="*", help="All files to upload")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_main()

    if args.sandbox:
        zenodo = ZenStorage(key=os.environ["ZENODO_TEST_KEY"], testing=True)
    else:
        # Because this is still just in development!
        zenodo = ZenStorage(key=os.environ["ZENODO_TEST_KEY"], testing=True)

    if args.deposition == "eia860_source":
        metadata = zs.metadata.eia860_source
        metadata["title"] += ": Test #%d" % 8499  # TODO: REMOVE THIS
        datapackager = frictionless.eia860.datapackager
    else:
        raise ValueError("Unsupported archive: %s" % args.deposition)

    if args.initialize:
        if args.noop:
            sys.exit()
        initial_run(zenodo, metadata, datapackager, args.files)
        sys.exit()

    local = local_fileinfo(args.files)

    deposition = zenodo.get_deposition('title: "%s"' % metadata["title"])

    if deposition is None:
        raise ValueError("Deposition not found. You may need to --initialize")

    remote = remote_fileinfo(zenodo, deposition)
    steps = action_steps(local, remote)

    if args.noop:
        print(json.dumps(steps, indent=4, sort_keys=True))
        sys.exit()

    execute_actions(zenodo, deposition, datapackager, steps)
