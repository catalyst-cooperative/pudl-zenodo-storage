"""Datapackage details specific to the EPACEMS unitid - EIA plant Crosswalk archives."""

from pudl.metadata.classes import DataSource
from pudl_zenodo_storage.frictionless.core import DataPackage, minimal_archiver


def datapackager(dfiles):
    """
    Produce the datapackage json for the epacems_unitid_eia_plant_crosswalk archive.

    Args:
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/
    """
    return DataPackage.from_resource_archiver(
        DataSource.from_id("epacems_unitid_eia_plant_crosswalk"),
        dfiles,
        minimal_archiver,
    ).to_raw_datapackage_dict()
