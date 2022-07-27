"""Provide datapackage details specific to the EIA Form 923 archives."""

from pudl.metadata.classes import DataSource
from pudl_zenodo_storage.frictionless.core import DataPackage, annual_archive_resource


def datapackager(dfiles):
    """
    Produce the datapackage json for the eia923 archival collection.

    Args:
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/
    """
    return DataPackage.from_resource_archiver(
        DataSource.from_id("eia923"), dfiles, annual_archive_resource
    ).to_raw_datapackage_dict()
