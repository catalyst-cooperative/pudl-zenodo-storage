# -*- coding: utf-8 -*-

from datetime import datetime, timezone
import re

from enum import Enum


class MediaType(Enum):
    """Enumerate file extention -> mediatype descriptors"""
    zip = "application/zip"


def annual_archive_resource(name, url, size, md5_hash):
    """
    Produce the resource descriptor for a single file

    Args:
        name: str, file name: must include a 4 digit year, and no other 4 digits
        url: str, url to download the file from Zenodo
        size: int, size it bytes
        md5_hash: str, the md5 checksum of the file

    Return: None
    """
    match = re.search(r"([\d]{4})", name)

    if match is None:
        raise ValueError("No year present in filename %s" % name)

    year = int(match.groups()[0])
    title, file_format = name.split(".")
    mt = MediaType[file_format].value

    return {
        "profile": "data-resource",
        "name": name,
        "path": url,
        "title": title,
        "parts": {"year": year},
        "encoding": "utf-8",
        "mediatype": mt,
        "format": file_format,
        "bytes": size,
        "hash": md5_hash
    }


def annual_resource_datapackager(metadata, dfiles):
    """
    Produce the datapackage json for a collection of annually named files.

    Args:
        metadata: dict of fixed metadata descriptors
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict of fields suited to the frictionless datapackage spec
            https://frictionlessdata.io/specs/data-package/
    """
    resources = [
        annual_archive_resource(
            x["filename"],
            x["links"]["self"],
            x["filesize"], x["checksum"])
        for x in dfiles]

    return dict(**metadata,
                **{"resources": resources,
                   "created": datetime.now(timezone.utc).isoformat()})
