"""Provide datapackage details specific to the EIP Infrastructure archives."""

from . import core
from . import contributors
from . import licenses

eipinfrastructure = {
    "name": "raw-eipinfrastructure",
    "title": "Raw EIP Infrastructure",
    "description":
        "The Environmental Integrity Project created this public database to "
        "track the environmental and human health impacts of 429 of the largest "
        "projects to build or expand capacity at gas processors, liquefied natural "
        "gas terminals, refineries, petrochemical plants, and fertilizer manufacturers."
        " The database also includes 116 interstate natural gas pipeline projects that " 
        "are under construction or recently completed, or that have been announced or "
        "approved by the Federal Energy Regulatory Commission.",
    "profile": "data-package",
    "keywords": [
        "eip", "usa", "electricity", "infrastructure", "fossil fuel", "emissions", "oil", "gas", "chemicals", "pipelines",
    ],
    "licenses": [licenses.us_govt, ],
    "homepage": "https://catalyst.coop/pudl/",
    "sources": [
        {
            "title": "Enivonrmental Integrity Project",
            "path": "https://environmentalintegrity.org/oil-gas-infrastructure-emissions/"
        }
    ],
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
    return core.minimal_datapackager(eipinfrastructure, dfiles)