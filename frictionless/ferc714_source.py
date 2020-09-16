# -*- coding: utf-8 -*-
"""Provide datapackage details specific to the Ferc Form 714 archives."""

from . import core
from . import contributors
from . import licenses

ferc714_source = {
    "name": "pudl-raw-ferc714",
    "title": "PUDL Raw FERC Form 714",
    "description":
        "Form 714 Annual Electric Balancing Authority Area and Planning Area "
        "Report from the Federal Energy Regulatory Commission (FERC).",
    "profile": "data-package",
    "keywords": [
        'electricity', 'electric', 'utility', 'plant', 'steam', 'generation',
        'cost', 'expense', 'price', 'heat content', 'ferc', 'form 714',
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
            "path": "https://www.ferc.gov/industries-data/electric/"
                    "general-information/electric-industry-forms/"
                    "form-no-714-annual-electric/data"
        }
    ],
    "contributors": [contributors.catalyst_cooperative]
}


def datapackager(dfiles):
    """
    Produce the datapackage json for the ferc714 archival collection.

    Args:
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/

    """
    return core.minimal_datapackager(ferc714_source, dfiles)
