"""Provide datapackage details specific to the Ferc Form 714 archives."""

from pudl.metadata.classes import DataSource

from .core import DataPackage, minimal_archiver


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
    return DataPackage.from_resource_archiver(
        DataSource.from_id("ferc714"),
        dfiles,
        minimal_archiver
    ).to_raw_datapackage_dict()
