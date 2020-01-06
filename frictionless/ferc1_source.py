# -*- coding: utf-8 -*-

from . import core
from . import licenses
from . import contributors

"""
Provide datapackage details specific to the Eia860 archives
"""

ferc1_source = {
    "name": "FERC Form No. 1",
    "title": "FERC Form No. 1",
    "description":
        "Form No. 1 financial and operating report from the Federal Energy "
        "regulatory commission.",

    "profile": "data-package",
    "keywords": [
        'electricity', 'electric', 'utility', 'plant', 'steam', 'generation',
        'cost', 'expense', 'price', 'heat content', 'ferc', 'form 1',
        'federal energy regulatory commission', 'capital', 'accounting',
        'depreciation', 'finance', 'plant in service', 'hydro', 'coal',
        'natural gas', 'gas', 'opex', 'capex', 'accounts', 'investment',
        'capacity'
    ],
    "licenses": [licenses.us_govt, licenses.cc_by],
    "homepage": "https://catalyst.coop/pudl/",
    "sources": [
        {
            "title": "Federal Energy Regulatory Commission",
            "path": "https://www.ferc.gov/docs-filing/forms/form-1/data.asp"
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
    return core.annual_resource_datapackager(ferc1_source, dfiles)
