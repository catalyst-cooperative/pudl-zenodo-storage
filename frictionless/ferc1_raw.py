# -*- coding: utf-8 -*-
"""Provide datapackage details specific to the FERC Form 1 archives."""

from . import core
from . import licenses
from . import contributors

ferc1_raw = {
    "name": "pudl-raw-ferc1",
    "title": "PUDL Raw FERC Form 1",
    "description":
        "The Federal Energy Regulatory Commission (FERC) Form 1 is a comprehensive "
        "financial and operating report submitted annually for electric rate "
        "regulation, market oversight analysis, and financial audits by Major "
        "electric utilities, licensees and others.",
    "profile": "data-package",
    "keywords": [
        'electricity', 'electric', 'utility', 'plant', 'steam', 'generation',
        'cost', 'expense', 'price', 'heat content', 'ferc', 'form 1',
        'federal energy regulatory commission', 'capital', 'accounting',
        'depreciation', 'finance', 'plant in service', 'hydro', 'coal',
        'natural gas', 'gas', 'opex', 'capex', 'accounts', 'investment',
        'capacity'
    ],
    "licenses": [licenses.us_govt, ],
    "homepage": "https://catalyst.coop/pudl/",
    "sources": [
        {
            "title": "Federal Energy Regulatory Commission (FERC)",
            "path": "https://www.ferc.gov/industries-data/electric/"
                    "general-information/electric-industry-forms/"
                    "form-1-electric-utility-annual"
        }
    ],
    "contributors": [contributors.catalyst_cooperative]
}


def datapackager(dfiles):
    """
    Produce the datapackage json for the ferc1 archival collection.

    Args:
        metadata: dict of fixed metadata descriptors

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/

    """
    return core.annual_resource_datapackager(ferc1_raw, dfiles)
