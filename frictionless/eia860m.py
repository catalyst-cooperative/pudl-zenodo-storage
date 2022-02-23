# -*- coding: utf-8 -*-
"""Datapackage details specific to the EIA Form 860 archives."""

from .core import DataPackage, archive_resource_year_month
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
    return DataPackage.from_resource_archiver(
        DataSource.from_id("eia860m"),
        dfiles,
        archive_resource_year_month
    ).to_raw_datapackage_dict()
