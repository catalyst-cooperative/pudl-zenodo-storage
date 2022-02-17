# -*- coding: utf-8 -*-
"""Datapackage details specific to the EIA Form 860 archives."""

from . import core
from pudl.metadata.classes import DataSource


def datapackager(dfiles):
    """
    Produce the datapackage json for the eia860 archival collection.

    Args:
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/
    """
    return core.annual_resource_datapackager(
        DataSource.from_id("eia860").to_raw_datapackage_dict(), dfiles)
