"""Datapackage details specific to the EIA Bulk Electricity archives."""

from pudl.metadata.classes import DataSource
from pudl_zenodo_storage.frictionless.core import DataPackage, minimal_archiver


def datapackager(dfiles):
    """
    Produce the datapackage json for the eia_bulk_elec archive.

    Args:
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/
    """
    return DataPackage.from_resource_archiver(
        DataSource.from_id("eia_bulk_elec"),
        dfiles,
        minimal_archiver,
    ).to_raw_datapackage_dict()
