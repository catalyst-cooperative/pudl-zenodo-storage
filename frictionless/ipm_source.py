# -*- coding: utf-8 -*-

from datetime import datetime, timezone
import re


from . import core
from . import licenses
from . import contributors

"""
Provide datapackage details specific to the Eia860 archives
"""

ipm_source = {
    "name": "IPM Source",
    "title": "IPM Source",
    "description": "EPA National Electric Energy Data System data, archived "
                   "from https://www.epa.gov/airmarkets/"
                   "national-electric-energy-data-system-needs-v6",
    "profile": "data-package",
    "keywords": ["epa", "ipm", "needs", "usa", "integrated planning"],
    "licenses": [licenses.us_govt, licenses.cc_by],
    "homepage": "https://catalyst.coop/pudl/",
    "sources": [
        {
            "title": "US Environmental Protection Agency",
            "path": "https://www.epa.gov/airmarkets/"
                    "national-electric-energy-data-system-needs-v6"
        }
    ],
    "contributors": [contributors.catalyst_cooperative]
}


def ipm_resource(name, url, size, md5_hash):
    """
    Produce the resource descriptor for a single file

    Args:
        name: str, file name: must include a 4 digit year, and no other 4 digits
        url: str, url to download the file from Zenodo
        size: int, size it bytes
        md5_hash: str, the md5 checksum of the file

    Return: frictionless datapackage file resource descriptor, per
            https://frictionlessdata.io/specs/data-resource/
    """
    match = re.search(r"([\d]{4})-([\d]{2})-([\d]{2})", name)

    if match is None:
        raise ValueError("No date found in %s" % name)

    year, month, day = [int(x) for x in match.groups()]
    title, file_format = name.split(".")
    mt = core.MediaType[file_format].value

    return {
        "profile": "data-resource",
        "name": name,
        "path": url,
        "title": title,
        "parts": {"year": year, "month": month, "day": day},
        "encoding": "utf-8",
        "mediatype": mt,
        "format": file_format,
        "bytes": size,
        "hash": md5_hash
    }


def datapackager(dfiles):
    """
    Produce the datapackage json for the IPM archival collection.

    Arguments:
        dfiles: a list of file descriptor dictionaries as expected from Zenodo,
                per https://developers.zenodo.org/#deposition-files

    Returns:
        dict of fields suited to the frictionless datapackage spec
            https://frictionlessdata.io/specs/data-package/
    """
    resources = [
        ipm_resource(
            x["filename"], 
            x["links"]["self"],
            x["filesize"], x["checksum"])
        for x in dfiles]

    return dict(**ipm_source,
                **{"resources": resources,
                   "created": datetime.now(timezone.utc).isoformat()})
