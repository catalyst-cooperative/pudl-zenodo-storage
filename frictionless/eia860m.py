# -*- coding: utf-8 -*-
"""Datapackage details specific to the EIA Form 860 archives."""

from . import core
from pudl.metadata.classes import DataSource


def datapackager(dfiles):
    """
    Produce the datapackage json for the eia860m archival collection.

    Args:
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/
    """
    return core.resource_datapackager_year_month(
        DataSource.from_id("eia860m").to_raw_datapackage_json(), dfiles)
