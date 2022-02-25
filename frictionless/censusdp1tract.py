# -*- coding: utf-8 -*-
"""Provide datapackage details specific to the Census DP1 data."""

from pudl.metadata.classes import DataSource

from .core import DataPackage, annual_archive_resource


def datapackager(dfiles):
    """
    Produce the datapackage json for the census archival collection.

    Args:
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/

    """
    return DataPackage.from_resource_archiver(
        DataSource.from_id("censusdp1tract"), dfiles, annual_archive_resource
    ).to_raw_datapackage_dict()
