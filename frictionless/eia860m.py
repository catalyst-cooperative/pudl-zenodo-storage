# -*- coding: utf-8 -*-
"""Datapackage details specific to the EIA Form 860 archives."""

from . import core
from . import licenses
from . import contributors

eia860m = {
    "name": "pudl-raw-eia860m",
    "title": "PUDL Raw EIA Form 860M",
    "description":
        "US Energy Information Administration (EIA) Form 860 M data for "
        "electric power plants with 1 megawatt or greater combined nameplate "
        "capacity. Preliminary Monthly Electric Generator Inventory (based on "
        "Form EIA-860M as a supplement to Form EIA-860)",
    "profile": "data-package",
    "keywords": [
        "preliminary", "year to date", "electricity", "electric", "boiler",
        "generator", "plant", "utility", "fuel", "coal", "natural gas",
        "prime mover", "eia860m", "eia860", "retirement", "capacity",
        "planned", "proposed", "energy", "hydro", "solar", "wind", "nuclear",
        "form 860M", "eia", "annual", "gas", "ownership", "steam", "turbine",
        "combustion", "combined cycle", "eia",
        "energy information administration", "usa"
    ],
    "licenses": [licenses.us_govt, ],
    "homepage": "https://catalyst.coop/pudl/",
    "sources": [
        {
            "title": "US Energy Information Administration",
            "path": "https://www.eia.gov/electricity/data/eia860m/"
        }
    ],
    "contributors": [contributors.catalyst_cooperative]
}


def datapackager(dfiles):
    """
    Produce the datapackage json for the eia860m archival collection.

    Args:
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/
    """
    return core.resource_datapackager_year_month(eia860m, dfiles)
