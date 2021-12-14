"""Provide datapackage details specific to the EIP Infrastructure archives."""

from . import core
from . import contributors
from . import licenses

lbnlisoqueues = {
    "name": "raw-lbnlisoqueues",
    "title": "Raw LBLN ISO Interconnection Queues",
    "description":
        "Berkeley Lab compiled and analyzed data from all seven ISOs/RTOs " 
        "in concert with 35 non-ISO utilities, representing an estimated "
        "85% of all U.S. electricity load. We include all 'active' projects "
        "in these generation interconnection queues through the end of 2020, "
        "as well as data on 'completed' and 'withdrawn' projects for five of "
        "the ISOs (CAISO, ISO-NE, MISO, NYISO, PJM).",
    "profile": "data-package",
    "keywords": [
        "lbln", "usa", "electricity", "iso", "renewables", "emissions", "utilities", "iso", "interconnection",
    ],
    "licenses": [licenses.us_govt, ],
    "homepage": "https://catalyst.coop/pudl/",
    "sources": [
        {
            "title": "LBLN ISO Interconnection Queues",
            "path": "https://emp.lbl.gov/publications/queued-characteristics-power-plants"
        }
    ],
    "contributors": [contributors.catalyst_cooperative]
}


def datapackager(dfiles):
    """
    Produce the datapackage json for the eipinfrastructure archival collection.

    Args:
        dfiles: iterable of file descriptors, as expected from Zenodo.
            https://developers.zenodo.org/#deposition-files

    Returns:
        dict: fields suited to the frictionless datapackage spec
        https://frictionlessdata.io/specs/data-package/

    """
    return core.minimal_datapackager(lbnlisoqueues, dfiles)