# -*- coding: utf-8 -*-

from . import core
from . import contributors
from . import licenses

"""
Provide datapackage details specific to the census data.
"""

census_source = {
    "name": "GeoData from the 2010 Census",
    "title": "GeoData from the 2010 Census",
    "description": "GeoData from the 2010 Census, archived from "
                   "http://www2.census.gov/geo/tiger/TIGER2010DP1/"
                   "Profile-County_Tract.zip",
    "profile": "data-package",
    "keywords": ['geodata', 'usa', 'census'],
    "licenses": [licenses.us_govt, licenses.cc_by],
    "homepage": "https://catalyst.coop/pudl/",
    "sources": [
        {
            "title": "US Census",
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
        dict of fields suited to the frictionless datapackage spec
            https://frictionlessdata.io/specs/data-package/
    """
    return core.minimal_datapackager(census_source, dfiles)
