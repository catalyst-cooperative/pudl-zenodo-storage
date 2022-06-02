# -*- coding: utf-8 -*-
"""Datapackage details specific to the EPA-EIA Crosswalk archives."""

from pudl.metadata.classes import DataSource

from .core import DataPackage, minimal_archiver


def datapackager(dfiles):
    """
    Produce the datapackage json for the epa-eia-crosswalk archival collection.

    Args:
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/
    """
    return DataPackage.from_resource_archiver(
        DataSource.from_id("epa_eia_crosswalk"), dfiles, minimal_archiver
    ).to_raw_datapackage_dict()
