# -*- coding: utf-8 -*-

from . import core
from . import licenses
from . import contributors

"""
Provide datapackage details specific to the Eia861 archives
"""

eia861_source = {
    "name": "Eia861 Source",
    "title": "Eia861 Source",
    "description":
        "Annual Electric Power Industry Report, Form EIA-861 detailed data "
        "files",
    "profile": "data-package",
    "keywords": [
        'electricity', 'electric', 'boiler', 'generator', 'plant', 'utility',
        'fuel', 'coal', 'natural gas', ' prime mover', 'eia861', 'retirement',
        'capacity', 'planned', 'proposed', 'energy', 'hydro', 'solar', 'wind',
        'nuclear', 'form 861', 'eia', 'annual', 'gas', 'ownership', 'steam',
        'turbine', 'combustion', 'combined cycle', 'eia',
        'energy information administration'
    ],
    "licenses": [licenses.us_govt, licenses.cc_by],
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
        dict of fields suited to the frictionless datapackage spec
            https://frictionlessdata.io/specs/data-package/
    """
    return core.annual_resource_datapackager(eia861_source, dfiles)
