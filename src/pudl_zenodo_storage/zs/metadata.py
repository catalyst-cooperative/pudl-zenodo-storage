# -*- coding: utf-8 -*-
"""Metadata for Zenodo depositions archiving PUDL raw input data."""

from typing import List

from pudl.metadata.classes import DataSource

pudl_description = """
<p>This archive contains raw input data for the Public Utility Data Liberation (PUDL)
software developed by <a href="https://catalyst.coop">Catalyst Cooperative</a>. It is
organized into <a href="https://specs.frictionlessdata.io/data-package/">Frictionless
Data Packages</a>. For additional information about this data and PUDL, see the
following resources:
<ul>
  <li><a href="https://github.com/catalyst-cooperative/pudl">The PUDL Repository on GitHub</a></li>
  <li><a href="https://readthedocs.org/projects/catalystcoop-pudl/">PUDL Documentation</a></li>
  <li><a href="https://zenodo.org/communities/catalyst-cooperative/">Other Catalyst Cooperative data archives</a></li>
</ul>
</p>
"""


def _parse_contributor_metadata(pudl_contributors) -> List[dict]:
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


def _generate_metadata(data_source_id, data_source_uuid):
    # if data_source_id == "eipinfrastructure":
    #    data_source = DataSource(**pzs.frictionless.eipinfrastructure.eipinfrastructure)
    # else:
    data_source = DataSource.from_id(data_source_id)

    return {
        "title": f"PUDL Raw {data_source.title}",
        "language": "eng",
        "upload_type": "dataset",
        "description": f"<p>{data_source.description} Archived from\n"
        f'<a href="{data_source.path}">{data_source.path}</a></p>'
        f"{pudl_description}",
        "creators": _parse_contributor_metadata(data_source.contributors),
        "access_right": "open",
        "license": data_source.license_raw.name,
        "keywords": [*data_source.keywords, data_source_uuid],
    }


# Unaltered Eia860 archive.
eia860_uuid = "a93cdabd-706f-48c7-ae02-4463dacf1419"
eia860 = _generate_metadata("eia860", eia860_uuid)

# Unaltered EIA860M archive.
eia860m_uuid = "863ba550-1faa-11eb-8dfb-a45e60b93f07"
eia860m = _generate_metadata("eia860m", eia860m_uuid)

# Unaltered Eia861 archive.
eia861_uuid = "70999ef2-50e9-47ae-a4f6-5d69e6ff98d1"
eia861 = _generate_metadata("eia861", eia861_uuid)

# Unaltered Eia923 archive.
eia923_uuid = "53831f63-fa82-475a-bef4-5b5f0b7c41a4"
eia923 = _generate_metadata("eia923", eia923_uuid)

# Unaltered EPA CEMS archive
epacems_uuid = "8bd99e7d-b11a-4bd1-8af0-bccf984dcc43"
epacems = _generate_metadata("epacems", epacems_uuid)

# Unaltered EPACEMS-EIA Crosswalk archive.
epacems_unitid_eia_plant_crosswalk_uuid = "40696588-d6ee-11ec-abb9-34363bce6e4c"
epacems_unitid_eia_plant_crosswalk = _generate_metadata(
    "epacems_unitid_eia_plant_crosswalk", epacems_unitid_eia_plant_crosswalk_uuid
)

# For the unaltered Ferc1 archive.
ferc1_uuid = "d3d91c87-c595-49d5-a7f3-e5f5669c8306"
ferc1 = _generate_metadata("ferc1", ferc1_uuid)

# For the unaltered Ferc2 archive.
ferc2_uuid = "894a87fd-cc94-46d1-903a-44be6e77d450"
ferc2 = _generate_metadata("ferc2", ferc2_uuid)

# Unaltered Ferc714 archive.
ferc714_uuid = "f31f0894-639e-4bc2-9b7f-8a84713bcc87"
ferc714 = _generate_metadata("ferc714", ferc714_uuid)

# For the census archive.
censusdp1tract_uuid = "beb36017-3fca-49be-a93a-7298f30ca3a3"
censusdp1tract = _generate_metadata("censusdp1tract", censusdp1tract_uuid)

# EIP Infrastructure archive.
# eipinfrastructure_uuid = "865a4ee2-5140-11ec-81d1-acde48001122"
# eipinfrastructure = _generate_metadata("eipinfrastructure", eipinfrastructure_uuid)
