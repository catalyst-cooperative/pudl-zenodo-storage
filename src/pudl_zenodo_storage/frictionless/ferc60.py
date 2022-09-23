"""Provide datapackage details specific to the FERC Form 60 archives."""

from pudl.metadata.classes import DataSource
from pudl_zenodo_storage.frictionless.core import (
    DataPackage,
    ferc_annual_archive_resource,
)


def datapackager(dfiles):
    """
    Produce the datapackage json for the ferc60 archival collection.

    Args:
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/

    """
    return DataPackage.from_resource_archiver(
        DataSource.from_id("ferc60"), dfiles, ferc_annual_archive_resource
    ).to_raw_datapackage_dict()
