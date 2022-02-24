from pathlib import Path
from datetime import datetime
import os.path
import re
from pydantic import BaseModel, AnyHttpUrl
from enum import Enum
from typing import Dict, List
from pudl.metadata.classes import Datetime, License, Contributor
from pudl.metadata.constants import CONTRIBUTORS


class MediaType(Enum):
    """Enumerate file extention -> mediatype descriptors."""

    zip = "application/zip"
    xlsx = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    csv = "text/csv"


class Resource(BaseModel):
    """
    Data resource

    See https://specs.frictionlessdata.io/data-resource.
    """

    profile: str = "data-resource"
    name: str
    path: AnyHttpUrl
    remote_url: AnyHttpUrl
    title: str
    parts: Dict
    encoding: str = "utf-8"
    mediatype: str
    format: str
    bytes: int
    hash: str


class DataPackage(BaseModel):
    """
    Data package

    See https://specs.frictionlessdata.io/data-package.
    """

    name: str
    title: str
    description: str
    keywords: List[str]
    contributors: List[Contributor]
    sources: List[Dict[str, str]]
    profile: str = "data-package"
    homepage: str = "https://catalyst.coop/pudl/"
    licenses: List[License]
    resources: List[Resource]
    created: Datetime

    @classmethod
    def from_resource_archiver(cls, data_source, dfiles, archiver):
        """
        Construct DataPackage from DataSource and archiver function.

        Args:
            data_source: DataSource object.
            dfiles: iterable of file descriptors, as expected from Zenodo.
                https://developers.zenodo.org/#deposition-files
            archiver: Callable that constructs Resource from file descriptor.

        Returns:
            DataPackage
        """
        resources = [
            archiver(
                x["filename"],
                x["links"]["download"],
                x["filesize"], x["checksum"])
            for x in dfiles]

        base_dict = data_source.dict(
            exclude={"field_namespace", "working_partitions", "license_pudl",
                     "contributors"})

        base_dict.update(
            name=f"pudl-raw-{base_dict['name']}",
            title=f"PUDL Raw {base_dict['title']}",
            sources=[{"title": base_dict["title"], "path": base_dict.pop("path")}],
            licenses=[base_dict.pop("license_raw")],
            resources=resources,
            contributors=[CONTRIBUTORS["catalyst-cooperative"]],
            created=datetime.utcnow()
        )

        return cls(**base_dict)

    def to_raw_datapackage_dict(self):
        """
        Return raw data-package descriptor.
        See https://specs.frictionlessdata.io/data-package
        """
        descriptor = self.dict()

        descriptor.update(
            created=descriptor["created"].isoformat()
        )

        return descriptor


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


def archive_resource_year_month(name, url, size, md5_hash):
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
    year_month = re.search(r"([\d]{4})-([\d]{2})", name)

    if year_month is None:
        raise ValueError(f"No year/month present in filename {name}")

    title, file_format = os.path.splitext(name)
    file_format = file_format[1:]
    mt = MediaType[file_format].value

    return {
        "profile": "data-resource",
        "name": name,
        "path": url,
        "remote_url": url,
        "title": title,
        "parts": {"year_month": year_month.group(0)},
        "encoding": "utf-8",
        "mediatype": mt,
        "format": file_format,
        "bytes": size,
        "hash": md5_hash
    }


def minimal_archiver(name, url, size, md5_hash):
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
