# -*- coding: utf-8 -*-
"""Datapackage details specific to the EIA Form 860 archives."""

from . import core
from . import licenses
from . import contributors

eia860 = {
    "name": "pudl-raw-eia860",
    "title": "PUDL Raw EIA Form 860",
    "description":
        "US Energy Information Administration (EIA) Form 860 data for electric power "
        "plants with 1 megawatt or greater combined nameplate capacity.",
    "licenses": [licenses.us_govt, ],
}

eia860.update(core.build_datapackage_from_id("eia860"))

def datapackager(dfiles):
    """
    Produce the datapackage json for the eia860 archival collection.

    Args:
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/
    """
    return core.annual_resource_datapackager(eia860, dfiles)
