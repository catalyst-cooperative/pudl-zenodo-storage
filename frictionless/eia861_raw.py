"""Provide datapackage details specific to the EIA 861 archives."""

from . import core
from . import licenses
from . import contributors

eia861_raw = {
    "name": "pudl-raw-eia861",
    "title": "PUDL Raw EIA Form 861",
    "description":
        "EIA Form 861 Annual Electric Power Industry Report, detailed data "
        "files.",
    "profile": "data-package",
    "keywords": [
        "electricity", "electric", "utility", "balancing area",
        "eia861", "sales", "energy efficiency", "dsm", "demand response",
        "demand side management", "service territory", "form 861", "eia",
        "energy information administration", "usa", "customers",
    ],
    "licenses": [licenses.us_govt, ],
    "homepage": "https://catalyst.coop/pudl/",
    "sources": [
        {
            "title": "US Energy Information Administration",
            "path": "https://www.eia.gov/electricity/data/eia861/"
        }
    ],
    "contributors": [contributors.catalyst_cooperative]
}


def datapackager(dfiles):
    """
    Produce the datapackage json for the eia861 archival collection.

    Args:
        metadata: dict of fixed metadata descriptors

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/
    """
    return core.annual_resource_datapackager(eia861_raw, dfiles)
