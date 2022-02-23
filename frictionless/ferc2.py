# -*- coding: utf-8 -*-
"""Provide datapackage details specific to the FERC Form 2 archives."""

from .core import DataPackage, annual_archive_resource
from pudl.metadata.classes import DataSource
from . import licenses
from . import contributors

ferc2 = {
    "name": "pudl-raw-ferc2",
    "title": "PUDL Raw FERC Form 2",
    "description":
        "The Federal Energy Regulatory Commission (FERC) Form 2 is a "
        "comprehensive financial and operating report submitted for "
        "natural gas pipelines rate regulation and financial audits.",
    "profile": "data-package",
    "keywords": [
        'utility', 'plant', 'steam', 'generation', 'energy',
        'cost', 'expense', 'price', 'heat content', 'ferc', 'form 2',
        'federal energy regulatory commission', 'capital', 'accounting',
        'depreciation', 'finance', 'plant in service',
        'natural gas', 'gas', 'opex', 'capex', 'accounts', 'investment',
        'capacity'
    ],
    "licenses": [licenses.us_govt, ],
    "homepage": "https://catalyst.coop/pudl/",
    "sources": [
        {
            "title": "Federal Energy Regulatory Commission (FERC)",
            "path": "https://www.ferc.gov/industries-data/natural-gas/"
                    "industry-forms/form-2-2a-3-q-gas-historical-vfp-data"
        }
    ],
    "contributors": [contributors.catalyst_cooperative]
}


def datapackager(dfiles):
    """
    Produce the datapackage json for the ferc2 archival collection.

    Args:
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/

    """
    return DataPackage.from_resource_archiver(
        DataSource.from_id("ferc2"),
        dfiles,
        annual_archive_resource
    ).to_raw_datapackage_dict()
