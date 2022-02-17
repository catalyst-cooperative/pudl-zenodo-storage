"""Provide datapackage details specific to the Ferc Form 714 archives."""

from . import core
from pudl.metadata.classes import DataSource


def datapackager(dfiles):
    """
    Produce the datapackage json for the ferc714 archival collection.

    Args:
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/

    """
    return core.minimal_datapackager(
        DataSource.from_id("ferc714").to_raw_datapackage_json(), dfiles)
