# -*- coding: utf-8 -*-
"""Provide datapackage details specific to the Census DP1 data."""

from . import core
from . import contributors
from . import licenses

censusdp1tract_raw = {
    "name": "pudl-raw-censusdp1tract",
    "title": "PUDL Raw Census DP1 Tract Geodatabase",
    "description": "US Census Demographic Profile 1 (DP1) County and Tract "
                   "GeoDatabase.",
    "profile": "data-package",
    "keywords": [
        "geodata", "usa", "census", "geodatabase", "gis", "spatial", "demographic",
        "dp1", "population", "county", "fips", "tract"
    ],
    "licenses": [licenses.us_govt, ],
    "homepage": "https://catalyst.coop/pudl/",
    "sources": [
        {
            "title": "US Census Bureau",
            "path": "http://www2.census.gov/geo/tiger/TIGER2010DP1/"
                    "Profile-County_Tract.zip",
        }
    ],
    "contributors": [contributors.catalyst_cooperative]
}


def datapackager(dfiles):
    """
    Produce the datapackage json for the census archival collection.

    Args:
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/

    """
    return core.annual_resource_datapackager(censusdp1tract_raw, dfiles)
