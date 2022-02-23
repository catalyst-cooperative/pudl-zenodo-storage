# -*- coding: utf-8 -*-
"""Provide datapackage details specific to the FERC Form 1 archives."""

from .core import DataPackage, annual_archive_resource
from pudl.metadata.classes import DataSource


def datapackager(dfiles):
    """
    Produce the datapackage json for the ferc1 archival collection.

    Args:
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/

    """
    return DataPackage.from_resource_archiver(
        DataSource.from_id("ferc1"),
        dfiles,
        annual_archive_resource
    ).to_raw_datapackage_dict()
