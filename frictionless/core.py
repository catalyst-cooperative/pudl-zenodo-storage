from pathlib import Path
from datetime import datetime, timezone
import os.path
import re

from enum import Enum


class MediaType(Enum):
    """Enumerate file extention -> mediatype descriptors."""

    zip = "application/zip"
    xlsx = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    csv = "text/csv"


def annual_archive_resource(name, url, size, md5_hash):
    """
    Produce the resource descriptor for a single file.

    Args:
        name (str): file name: must include a 4 digit year, and no other 4 digits.
        url (str): url to download the file from Zenodo.
        size (int): size in bytes.
        md5_hash (str): the md5 checksum of the file.

    Returns:
        dict: a frictionless data package resource descriptor, per
        https://frictionlessdata.io/specs/data-resource/

    """
    match = re.search(r"([\d]{4})", name)

    if match is None:
        raise ValueError(f"No year present in filename {name}")

    year = int(match.groups()[0])
    title, file_format = os.path.splitext(name)
    file_format = file_format[1:]
    mt = MediaType[file_format].value

    return {
        "profile": "data-resource",
        "name": name,
        "path": url,
        "remote_url": url,
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
        metadata (dict): fixed metadata descriptors.
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict of fields suited to the frictionless datapackage spec
            https://frictionlessdata.io/specs/data-package/
    """
    resources = [
        annual_archive_resource(
            x["filename"],
            x["links"]["download"],
            x["filesize"], x["checksum"])
        for x in dfiles]

    return dict(**metadata,
                **{"resources": resources,
                   "created": datetime.now(timezone.utc).isoformat()})


def minimal_datapackager(package_meta, dfiles):
    """
    Produce the datapackage json for the given archival collection.

    Args:
        package_meta (dict): required package metadata, per the frictionless spec,
            excluding resources.
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/

    """
    def resource_descriptor(dfile):

        name = dfile["filename"]
        url = dfile["links"]["download"]
        size = dfile["filesize"]
        md5_hash = dfile["checksum"]

        fp = Path(name)
        title = fp.stem
        file_format = fp.suffix[1:]
        mt = MediaType[file_format].value

        return {
            "profile": "data-resource",
            "name": name,
            "path": url,
            "title": title,
            "remote_url": url,
            "parts": {},
            "encoding": "utf-8",
            "mediatype": mt,
            "format": file_format,
            "bytes": size,
            "hash": md5_hash
        }

    resources = [resource_descriptor(df) for df in dfiles]

    return dict(**package_meta,
                **{"resources": resources,
                   "created": datetime.now(timezone.utc).isoformat()})
