"""Metadata for Zenodo depositions archiving PUDL raw input data."""
from pudl.metadata.classes import Contributor, DataSource

UUIDS: dict[str, str] = {
    "censusdp1tract": "beb36017-3fca-49be-a93a-7298f30ca3a3",
    "eia860": "a93cdabd-706f-48c7-ae02-4463dacf1419",
    "eia860m": "863ba550-1faa-11eb-8dfb-a45e60b93f07",
    "eia861": "70999ef2-50e9-47ae-a4f6-5d69e6ff98d1",
    "eia923": "53831f63-fa82-475a-bef4-5b5f0b7c41a4",
    "eia_bulk_elec": "c288a5fe-1ff5-442d-a48e-7d56395bf72d",
    "epacamd_eia": "40696588-d6ee-11ec-abb9-34363bce6e4c",
    "epacems": "8bd99e7d-b11a-4bd1-8af0-bccf984dcc43",
    "ferc1": "d3d91c87-c595-49d5-a7f3-e5f5669c8306",
    "ferc2": "894a87fd-cc94-46d1-903a-44be6e77d450",
    "ferc714": "f31f0894-639e-4bc2-9b7f-8a84713bcc87",
}

PUDL_DESCRIPTION = """
<p>This archive contains raw input data for the Public Utility Data Liberation (PUDL)
software developed by <a href="https://catalyst.coop">Catalyst Cooperative</a>. It is
organized into <a href="https://specs.frictionlessdata.io/data-package/">Frictionless
Data Packages</a>. For additional information about this data and PUDL, see the
following resources:
<ul>
  <li><a href="https://github.com/catalyst-cooperative/pudl">The PUDL Repository on GitHub</a></li>
  <li><a href="https://catalystcoop-pudl.readthedocs.io">PUDL Documentation</a></li>
  <li><a href="https://zenodo.org/communities/catalyst-cooperative/">Other Catalyst Cooperative data archives</a></li>
</ul>
</p>
"""


def _parse_contributor_metadata(
    pudl_contributors: list[Contributor],
) -> list[dict[str, str]]:
    """Reformat PUDL contributor metadata to fit Zenodo requirements."""
    zenodo_cont_list = []

    for contributor in pudl_contributors:
        pudl_cont_dict = contributor.dict()
        zenodo_cont_dict = {
            "name": pudl_cont_dict["title"],
            "affiliation": pudl_cont_dict["organization"],
        }
        zenodo_cont_list.append(zenodo_cont_dict)

    return zenodo_cont_list


def generate_metadata(data_source_id: str) -> dict[str, str]:
    """Construct the metadata required for a Zenodo deposition."""
    data_source = DataSource.from_id(data_source_id)

    return {
        "title": f"PUDL Raw {data_source.title}",
        "language": "eng",
        "upload_type": "dataset",
        "description": (
            f"<p>{data_source.description} Archived from\n"
            f'<a href="{data_source.path}">{data_source.path}</a></p>'
            f"{PUDL_DESCRIPTION}"
        ),
        "creators": _parse_contributor_metadata(data_source.contributors),
        "access_right": "open",
        "license": data_source.license_raw.name,
        "keywords": [*data_source.keywords, UUIDS[data_source_id]],
    }
