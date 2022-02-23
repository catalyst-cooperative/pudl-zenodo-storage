"""Provide datapackage details specific to the EIP Infrastructure archives."""

from . import contributors
from .core import DataPackage, minimal_archiver
from pudl.metadata.constants import LICENSES
from pudl.metadata.classes import DataSource

eipinfrastructure = {
    "name": "raw_eipinfrastructure",
    "title": "Raw EIP I",
    "path": "https://environmentalintegrity.org/oil-gas-infrastructure-emissions/",
    "description":
        "The Environmental Integrity Project created this public database to "
        "track the environmental and human health impacts of 429 of the largest "
        "projects to build or expand capacity at gas processors, liquefied natural "
        "gas terminals, refineries, petrochemical plants, and fertilizer manufacturers."
        " The database also includes 116 interstate natural gas pipeline projects that " 
        "are under construction or recently completed, or that have been announced or "
        "approved by the Federal Energy Regulatory Commission.",
    "keywords": [
        "eip", "usa", "electricity", "infrastructure", "fossil fuel", "emissions",
        "oil", "gas", "chemicals", "pipelines",
    ],
    "license_raw": LICENSES["us-govt"],
    "license_pudl": LICENSES["cc-by-4.0"],
    "contributors": [contributors.catalyst_cooperative]
}


def datapackager(dfiles):
    """
    Produce the datapackage json for the eipinfrastructure archival collection.

    Args:
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/

    """
    return DataPackage.from_resource_archiver(
        DataSource(**eipinfrastructure),
        dfiles,
        minimal_archiver
    ).to_raw_datapackage_dict()
