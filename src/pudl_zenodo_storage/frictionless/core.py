"""Core routines for frictionless data package construction."""
import os.path
import re
from datetime import datetime
from pathlib import Path

from pydantic import AnyHttpUrl, BaseModel

from pudl.metadata.classes import Contributor, Datetime, License
from pudl.metadata.constants import CONTRIBUTORS

MEDIA_TYPES: dict[str, str] = {
    "zip": "application/zip",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "csv": "text/csv",
}


class Resource(BaseModel):
    """
    A generic data resource, as per Frictionless Data specs.

    See https://specs.frictionlessdata.io/data-resource.
    """

    profile: str = "data-resource"
    name: str
    path: AnyHttpUrl
    remote_url: AnyHttpUrl
    title: str
    parts: dict
    encoding: str = "utf-8"
    mediatype: str
    format_: str
    bytes_: int
    hash_: str

    class Config:
        """Alias attributes using reserved Python keywords."""

        fields = {
            "format_": "format",
            "bytes_": "bytes",
            "hash_": "hash",
        }


class DataPackage(BaseModel):
    """
    A generic Data Package, as per Frictionless Data specs.

    See https://specs.frictionlessdata.io/data-package.
    """

    name: str
    title: str
    description: str
    keywords: list[str]
    contributors: list[Contributor]
    sources: list[dict[str, str]]
    profile: str = "data-package"
    homepage: str = "https://catalyst.coop/pudl/"
    licenses: list[License]
    resources: list[Resource]
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
                x["filename"], x["links"]["download"], x["filesize"], x["checksum"]
            )
            for x in dfiles
        ]

        base_dict = data_source.dict(
            exclude={
                "field_namespace",
                "working_partitions",
                "license_pudl",
                "contributors",
            }
        )

        base_dict.update(
            name=f"pudl-raw-{base_dict['name']}",
            title=f"PUDL Raw {base_dict['title']}",
            sources=[{"title": base_dict["title"], "path": base_dict.pop("path")}],
            licenses=[base_dict.pop("license_raw")],
            resources=resources,
            contributors=[CONTRIBUTORS["catalyst-cooperative"]],
            created=datetime.utcnow(),
        )

        return cls(**base_dict)

    def to_raw_datapackage_dict(self):
        """
        Return a data package descriptor.

        See https://specs.frictionlessdata.io/data-package
        """
        descriptor = self.dict(by_alias=True)

        descriptor.update(created=descriptor["created"].isoformat())

        return descriptor


def annual_archive_resource(name, url, size, md5_hash, **extra_parts):
    """
    Produce the resource descriptor for a single file.

    Args:
        name (str): file name: must include a 4 digit year, and no other 4 digits.
        url (str): url to download the file from Zenodo.
        size (int): size in bytes.
        md5_hash (str): the md5 checksum of the file.
        extra_parts (str): extra partitions to add to resource descriptor.

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
    mt = MEDIA_TYPES[file_format]

    return {
        "profile": "data-resource",
        "name": name,
        "path": url,
        "remote_url": url,
        "title": title,
        "parts": {"year": year, **extra_parts},
        "encoding": "utf-8",
        "mediatype": mt,
        "bytes": size,
        "hash": md5_hash,
        "format": file_format,
    }


def ferc_annual_archive_resource(name, url, size, md5_hash):
    """
    Produce the resource descriptor for a single file.

    FERC filers can resubmit past years in XBRL format. This means that
    there are years with both DBF and XBRL data. These will be saved in
    different archives, and an extra partition is added to the resource
    descriptor to indicate which data is contianed in each archive.

    Args:
        name (str): file name: must include a 4 digit year, and no other 4 digits.
        url (str): url to download the file from Zenodo.
        size (int): size in bytes.
        md5_hash (str): the md5 checksum of the file.

    Returns:
        dict: a frictionless data package resource descriptor, per
        https://frictionlessdata.io/specs/data-resource/

    """
    # Check file name to see if it contains XBRL data
    data_format = "XBRL" if "xbrl" in name else "DBF"

    return annual_archive_resource(name, url, size, md5_hash, data_format=data_format)


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
    mt = MEDIA_TYPES[file_format]

    return {
        "profile": "data-resource",
        "name": name,
        "path": url,
        "remote_url": url,
        "title": title,
        "parts": {"year_month": year_month.group(0)},
        "encoding": "utf-8",
        "mediatype": mt,
        "bytes": size,
        "hash": md5_hash,
        "format": file_format,
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
    mt = MEDIA_TYPES[file_format]

    return {
        "profile": "data-resource",
        "name": name,
        "path": url,
        "title": title,
        "remote_url": url,
        "parts": {},
        "encoding": "utf-8",
        "mediatype": mt,
        "bytes": size,
        "hash": md5_hash,
        "format": file_format,
    }
