"""Provide datapackage details specific to the EIA 861 archives."""

from . import core
from pudl.metadata.classes import DataSource


def datapackager(dfiles):
    """
    Produce the datapackage json for the eia861 archival collection.

    Args:
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/
    """
    return core.annual_resource_datapackager(
        DataSource.from_id("eia861").to_raw_datapackage_json(), dfiles)
