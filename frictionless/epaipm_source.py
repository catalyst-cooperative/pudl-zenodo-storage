# -*- coding: utf-8 -*-
"""Provide datapackage details specific to the EPA IPM/NEEDS archives."""

from datetime import datetime, timezone
import os.path
import re

from . import core
from . import licenses
from . import contributors

epaipm_source = {
    "name": "pudl-raw-epaipm",
    "title": "PUDL Raw EPA IPM/NEEDS",
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


def epaipm_resource(name, url, size, md5_hash):
    """
    Produce the resource descriptor for a single file.

    Args:
        name (str): file name: must include a 4 digit year, and no other 4 digits.
        url (str): url to download the file from Zenodo.
        size (int): size it bytes.
        md5_hash (str): the md5 checksum of the file.

    Returns:
        frictionless datapackage file resource descriptor, per
        https://frictionlessdata.io/specs/data-resource/

    """

    def make_parts():
        match = re.search(r"([\d]{4})-([\d]{2})-([\d]{2})", name)
        remote = {"remote_url": url}

        if match is not None:
            year, month, day = [int(x) for x in match.groups()]
            return {"year": year, "month": month, "day": day, **remote}

        match = re.search(r"(19|20)([\d]{2})", name)

        if match is not None:
            year = "".join(match.groups())
            return {"year": int(year), **remote}

        return remote

    title, file_format = os.path.splitext(name)
    file_format = file_format[1:]
    mt = core.MediaType[file_format].value
    parts = make_parts()

    return {
        "profile": "data-resource",
        "name": name,
        "path": url,
        "title": title,
        "parts": parts,
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
        dfiles (list): file descriptor dictionaries as expected from Zenodo,
        per https://developers.zenodo.org/#deposition-files

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/

    """
    resources = [
        epaipm_resource(
            x["filename"],
            x["links"]["download"],
            x["filesize"], x["checksum"])
        for x in dfiles]

    return dict(**epaipm_source,
                **{"resources": resources,
                   "created": datetime.now(timezone.utc).isoformat()})
