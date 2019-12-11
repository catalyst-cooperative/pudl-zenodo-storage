#!/usr/bin/env python
# -*- coding: utf-8

import argparse
import io
import json
from hashlib import md5
import os
import random
import requests
import sys

import frictionless.eia860
from zs import ZenStorage
import zs.metadata


"""
zen_store.py --help
zen_store.py [--noop] [--test] eia860 ~/tmp/*.zip
"""


def local_md5s(file_paths):
    """
    Produce a dict describing file names, paths, and md5 hashes.

    Args:
        file_paths: a list file path strings, as provided from the CLI

    Returns:
        dict of form {filename: {path: str, hash: str (md5)}}
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
        file_hash = file_md5s(fp)

        if name in metadata:
            msg = "File names must be unique: %s name conflicts with %s/%s" % (
                path, metadata[name]["path"], name)
            raise ValueError(msg)

        metadata[name] = {"path": path, "hash": file_hash}

    return metadata


def initial_run(zenodo, metadata, datapackage, file_paths):
    """
    Create the first version of a Zenodo archive.

    Args:
        zenodo: a zs.ZenStorage manager
        metadata: the zen_store metadata (NOT frictionless datapackage data!) for
            the deposition, such as zen_store.metadata.eia860
        datapackage: the frictionless data package metadata, such as
            frictionless.eia860.eia860
        file_paths: a list of files to upload

    Returns:
        True on success, raises an error on failure
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

    # Save the datapackage.json
    fstr = json.dumps(datapackage, indent=4, sort_keys=True)
    fcontents = io.BytesIO(bytes(fstr, encoding="utf-8"))
    zenodo.bucket_api_upload(deposition, "datapackage.json", fcontents)

    # Upload all requested files
    for fp in file_paths:
        path, name = os.path.split(fp)

        with open(fp, "rb") as f:
            zenodo.bucket_api_upload(deposition, name, f)

    # Publish
    response = requests.post(
            deposition["links"]["publish"], data={"access_token": zenodo.key})
    jsr = response.json()

    if response.status_code > 299:
        msg = "Failed to publish %s: %s" % (metadata["title"], json.dumps(jsr))
        raise RuntimeError(msg)

    return True


def parse_main():
    """
    Process base commands from the CLI
    """
    parser = argparse.ArgumentParser(
        description="Upload PUDL data archives to Zenodo")
    parser.add_argument("--noop", action="store_true",
                        help="Review changes without uploading")
    parser.add_argument("--sandbox", action="store_true",
                        help="Use Zenodo sandbox server")
    parser.add_argument(
        "--initialize", action="store_true",
        help="Produce the first version of a new Zenodo deposition.")
    parser.add_argument("deposition", help="Name of the Zenodo deposition."
                        " Supported: eia860")

    parser.add_argument("files", nargs="*", help="All files to upload")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_main()

    if args.sandbox:
        zenodo = ZenStorage(key=os.environ["ZENODO_TEST_KEY"], testing=True)
    else:
        # Because this is still just in development!
        zenodo = ZenStorage(key=os.environ["ZENODO_TEST_KEY"], testing=True)

    if args.deposition == "eia860":
        metadata = zs.metadata.eia860_source
        metadata["title"] += ": Test #%d" % random.randint(1000, 9999)
        fl = frictionless.eia860.eia860
    else:
        raise ValueError("Unsupported archive: %s" % args.deposition)

    if args.initialize:
        if args.noop:
            sys.exit()
        initial_run(zenodo, metadata, fl, args.files)
        sys.exit()
