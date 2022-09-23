"""Provide datapackage details specific to the Ferc Form 714 archives."""
import re

from pudl.metadata.classes import DataSource
from pudl_zenodo_storage.frictionless.core import (
    DataPackage,
    annual_archive_resource,
    minimal_archiver,
)


def datapackager(dfiles):
    """
    Produce the datapackage json for the ferc714 archival collection.

    Args:
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/

    """
    return DataPackage.from_resource_archiver(
        DataSource.from_id("ferc714"), dfiles, archive_714
    ).to_raw_datapackage_dict()


def archive_714(name: str, url: str, size: int, md5_hash: str):
    """Archiver wrapper for FERC 714 data.

    Historical DBF data is archived in a single zip file across all years. New XBRL
    data is archived in annual files. This will check each file name, and use the
    appropriate archiver.

    Args:
        name: file name
        url: url to download the file from Zenodo.
        size: size in bytes.
        md5_hash: the md5 checksum of the file.

    Returns:
        dict: a frictionless data package resource descriptor, per
        https://frictionlessdata.io/specs/data-resource/
    """
    # Check if year is in filename (minimum year is 2000)
    if re.search(r"2\d{3}", name):
        archive = annual_archive_resource(name, url, size, md5_hash)
    else:
        archive = minimal_archiver(name, url, size, md5_hash)

    return archive
