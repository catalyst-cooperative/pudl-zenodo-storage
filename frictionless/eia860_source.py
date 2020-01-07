# -*- coding: utf-8 -*-

from . import core
from . import licenses
from . import contributors

"""
Provide datapackage details specific to the Eia860 archives
"""

eia860_source = {
    "name": "Eia860 Source",
    "title": "Eia860 Source",
    "description":
        "Form Eia860 data for electric power plants with 1 megawatt "
        "greater compbined nameplate capacity.",

    "profile": "data-package",
    "keywords": [
        "electricity", "electric", "boiler", "generator", "plant", "utility",
        "fuel", "coal", "natural gas", " prime mover", "eia860", "retirement",
        "capacity", "planned", "proposed", "energy", "hydro", "solar", "wind",
        "nuclear", "form 860", "eia", "annual", "gas", "ownership", "steam",
        "turbine", "combustion", "combined cycle", "eia",
        "energy information administration"
    ],
    "licenses": [licenses.us_govt, licenses.cc_by],
    "homepage": "https://catalyst.coop/pudl/",
    "sources": [
        {
            "title": "US Energy Information Administration",
            "path": "https://www.eia.gov/electricity/data/eia860/"
        }
    ],
    "contributors": [contributors.catalyst_cooperative]
}


def datapackager(dfiles):
    """
    Produce the datapackage json for the eia860 archival collection.

    Args:
        metadata: dict of fixed metadata descriptors

    Returns:
        dict of fields suited to the frictionless datapackage spec
            https://frictionlessdata.io/specs/data-package/
    """
    return core.annual_resource_datapackager(eia860_source, dfiles)
