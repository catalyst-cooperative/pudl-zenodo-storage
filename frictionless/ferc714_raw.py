# -*- coding: utf-8 -*-
"""Provide datapackage details specific to the Ferc Form 714 archives."""

from . import core
from . import contributors
from . import licenses

ferc714_raw = {
    "name": "pudl-raw-ferc714",
    "title": "PUDL Raw FERC Form 714",
    "description":
        "Electric transmitting utilities operating balancing authority areas and "
        "planning areas with annual peak demand over 200MW are required to "
        "file Form 714 with the Federal Energy Regulatory Commission (FERC), "
        "reporting balancing authority area generation, actual and scheduled "
        "inter-balancing authority area power transfers, and net energy for "
        "load, summer-winter generation peaks and system lambda.",
    "profile": "data-package",
    "keywords": [
        'electricity', 'electric', 'utility', 'planning area', 'form 714',
        'balancing authority', 'demand', 'system lambda', 'ferc',
        'federal energy regulatory commission', "hourly", "generation",
        "interchange", "forecast", "load", "adjacency", "plants",
    ],
    "licenses": [licenses.us_govt, ],
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
    return core.minimal_datapackager(ferc714_raw, dfiles)
