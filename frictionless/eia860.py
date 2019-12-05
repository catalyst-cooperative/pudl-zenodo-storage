# -*- coding: utf-8 -*-

from . import licenses
from . import contributors

"""
Provide datapackage details specific to the Eia860 archives
"""

eia860 = {
    "name": "Eia860",
    "title": "Eia860",
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
