# -*- coding: utf-8 -*-

from . import core
from . import licenses
from . import contributors

"""
Provide datapackage details specific to the Eia860 archives
"""

eia923_source = {
    "name": "Eia 923: Source",
    "title": "Eia 923: Source",
    "description":
        "From the US Energy Information Administration:\n"
        "> The survey Form EIA-923 collects detailed electric power data -- "
        "monthly and annually -- on electricity generation, fuel "
        "consumption, fossil fuel stocks, and receipts at the power plant "
        "and prime mover level.",
    "profile": "data-package",
    "keywords": [
        "fuel", "boiler", "generator", "plant", "utility", "cost", "price",
        "natural gas", "coal", "eia923", "energy", "electricity", "form 923",
        "receipts", "generation", "net generation", "monthly", "annual", "gas",
        "fuel consumption", "MWh", "energy information administration", "eia",
        "mercury", "sulfur", "ash", "lignite", "bituminous", "subbituminous",
        "heat content"
    ],
    "licenses": [licenses.us_govt, licenses.cc_by],
    "homepage": "https://catalyst.coop/pudl/",
    "sources": [
        {
            "title": "US Energy Information Administration",
            "path": "https://www.eia.gov/electricity/data/eia923/"
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
    return core.annual_resource_datapackager(eia923_source, dfiles)
