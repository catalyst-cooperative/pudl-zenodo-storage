# -*- coding: utf-8 -*-

"""Metadata for Zenodo depositions archiving PUDL raw input data."""

creators = [
    {
        "name": "Gosnell, Christina",
        "affiliation": "Catalyst Cooperative"
    },
    {
        "name": "Selvans, Zane",
        "affiliation": "Catalyst Cooperative",
        "orcid": "0000-0002-9961-7208"
    }
]

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

# Unaltered Eia860 archive.
eia860_uuid = "a93cdabd-706f-48c7-ae02-4463dacf1419"
eia860 = {
    "title": "PUDL Raw EIA Form 860",
    "language": "eng",
    "upload_type": "dataset",
    "description": "<p>Raw US Energy Information Administration (EIA) Form 860 data, "
                   "archived from\n"
                   "<a href=\"https://www.eia.gov/electricity/data/eia860/\">"
                   "https://www.eia.gov/electricity/data/eia860/</a></p>"
                   f"{pudl_description}",
    "creators": creators,
    "access_right": "open",
    "license": "other-pd",
    "keywords": [
        "electricity", "electric", "boiler", "generator", "plant", "utility",
        "fuel", "coal", "natural gas", "prime mover", "eia860", "retirement",
        "capacity", "planned", "proposed", "energy", "hydro", "solar", "wind",
        "nuclear", "form 860", "eia", "annual", "gas", "ownership", "steam",
        "turbine", "combustion", "combined cycle", "eia",
        "energy information administration", "usa", eia860_uuid
    ]
}

# Unaltered EIA860M archive.
eia860m_uuid = "863ba550-1faa-11eb-8dfb-a45e60b93f07"
eia860m = {
    "title": "PUDL Raw EIA Form 860M",
    "language": "eng",
    "upload_type": "dataset",
    "description": "<p>Raw US Energy Information Administration (EIA) Form "
                   "860M data, archived from\n"
                   "<a href=\"https://www.eia.gov/electricity/data/eia860m/\">"
                   "https://www.eia.gov/electricity/data/eia860m/</a></p> "
                   f"{pudl_description}",
    "creators": creators,
    "access_right": "open",
    "license": "other-pd",
    "keywords": [
        "preliminary", "year to date", "electricity", "electric", "boiler",
        "generator", "plant", "utility", "fuel", "coal", "natural gas",
        "prime mover", "eia860m", "eia860", "retirement", "capacity",
        "planned", "proposed", "energy", "hydro", "solar", "wind", "nuclear",
        "form 860M", "eia", "annual", "gas", "ownership", "steam", "turbine",
        "combustion", "combined cycle", "eia",
        "energy information administration", "usa", eia860m_uuid
    ]
}

# Unaltered Eia861 archive.
eia861_uuid = "70999ef2-50e9-47ae-a4f6-5d69e6ff98d1"
eia861 = {
    "title": "PUDL Raw EIA Form 861",
    "language": "eng",
    "upload_type": "dataset",
    "description": "<p>Raw US Energy Information Administration (EIA) Form 861 Data, "
                   "archived from\n"
                   "<a href=\"https://www.eia.gov/electricity/data/eia861/\">"
                   "https://www.eia.gov/electricity/data/eia861/</a></p>"
                   f"{pudl_description}",
    "creators": creators,
    "access_right": "open",
    "license": "other-pd",
    "keywords": [
        "electricity", "electric", "utility", "balancing area",
        "eia861", "sales", "energy efficiency", "dsm", "demand response",
        "demand side management", "service territory", "form 861", "eia",
        "energy information administration", "usa", eia861_uuid
    ]
}


# Unaltered Eia923 archive.
eia923_uuid = "53831f63-fa82-475a-bef4-5b5f0b7c41a4"
eia923 = {
    "title": "PUDL Raw EIA Form 923",
    "language": "eng",
    "upload_type": "dataset",
    "description": "<p>Raw US Energy Information Administration (EIA) Form 923 data, "
                   "archived from\n"
                   "<a href=\"https://www.eia.gov/electricity/data/eia923/\">"
                   "https://www.eia.gov/electricity/data/eia923/</a></p>"
                   f"{pudl_description}",
    "creators": creators,
    "access_right": "open",
    "license": "other-pd",
    "keywords": [
        "fuel", "boiler", "generator", "plant", "utility", "cost", "price",
        "natural gas", "coal", "eia923", "energy", "electricity", "form 923",
        "receipts", "generation", "net generation", "monthly", "annual", "gas",
        "fuel consumption", "MWh", "energy information administration", "eia",
        "mercury", "sulfur", "ash", "lignite", "bituminous", "subbituminous",
        "heat content", eia923_uuid
    ]
}


# Unaltered EPA CEMS archive
epacems_uuid = "8bd99e7d-b11a-4bd1-8af0-bccf984dcc43"
epacems = {
    "title": "PUDL Raw EPA CEMS Hourly",
    "language": "eng",
    "upload_type": "dataset",
    "description": "<p>Raw US EPA hourly Continuous Emissions Monitoring System "
                   "(CEMS) data, archived from\n"
                   "<a href=\"ftp://newftp.epa.gov/dmdnload/emissions/hourly/monthly\">"
                   "ftp://newftp.epa.gov/dmdnload/emissions/hourly/monthly</a></p>"
                   f"{pudl_description}",
    "creators": creators,
    "access_right": "open",
    "license": "other-pd",
    "keywords": [
        "epa", "us", "emissions", "pollution", "ghg", "so2", "co2", "sox",
        "nox", "load", "utility", "electricity", "plant", "generator", "unit",
        "generation", "capacity", "output", "power", "heat content", "mmbtu",
        "steam", "cems", "continuous emissions monitoring system", "hourly"
        "environmental protection agency", "ampd", "air markets program data",
        epacems_uuid
    ]
}

# For the unaltered Ferc1 archive.
ferc1_uuid = "d3d91c87-c595-49d5-a7f3-e5f5669c8306"
ferc1 = {
    "title": "PUDL Raw FERC Form 1",
    "language": "eng",
    "upload_type": "dataset",
    "description": "<p>Raw Federal Energy Regulatory Commission (FERC) Form 1 data, "
                   "archived from\n"
                   "<a href=\"https://www.ferc.gov/industries-data/electric/"
                   "general-information/electric-industry-forms/"
                   "form-1-electric-utility-annual\">"
                   "https://www.ferc.gov/industries-data/electric/"
                   "general-information/electric-industry-forms/"
                   "form-1-electric-utility-annual</a></p>"
                   f"{pudl_description}",
    "creators": creators,
    "access_right": "open",
    "license": "other-pd",
    "keywords": [
        "electricity", "electric", "utility", "plant", "steam", "generation",
        "cost", "expense", "price", "heat content", "ferc", "form 1",
        "federal energy regulatory commission", "capital", "accounting",
        "depreciation", "finance", "plant in service", "hydro", "coal",
        "natural gas", "gas", "opex", "capex", "accounts", "investment",
        "capacity", "usa", ferc1_uuid
    ]
}

# Unaltered Ferc714 archive.
ferc714_uuid = "f31f0894-639e-4bc2-9b7f-8a84713bcc87"
ferc714 = {
    "title": "PUDL Raw FERC Form 714",
    "language": "eng",
    "upload_type": "dataset",
    "description": "<p>Federal Energy Regulatory Commission (FERC) Form 714 Data, "
                   "archived from\n"
                   "<a href=\"https://www.ferc.gov/industries-data/electric/"
                   "general-information/electric-industry-forms/"
                   "form-no-714-annual-electric/data\">"
                   "https://www.ferc.gov/industries-data/electric/"
                   "general-information/electric-industry-forms/"
                   "form-no-714-annual-electric/data</a></p>"
                   f"{pudl_description}",
    "creators": creators,
    "access_right": "open",
    "license": "other-pd",
    "keywords": [
        "electricity", "electric", "utility", "planning area", "form 714", "ferc714",
        "balancing authority", "demand", "system lambda", "ferc",
        "federal energy regulatory commission", "hourly", "generation",
        "interchange", "forecast", "load", "adjacency", "plants", ferc714_uuid
    ]
}

# For the unaltered IPM archive.
epaipm_uuid = "75b29994-bd39-4518-a5b2-ec180a18ac23"
epaipm = {
    "title": "PUDL Raw EPA IPM/NEEDS",
    "language": "eng",
    "upload_type": "dataset",
    "description": "<p>Select data pertaining to the US EPA Integrated Planning Model / "
                   "National Electric Energy Data System (IPM/NEEDS) "
                   "Archived from\n"
                   "<a href=\"https://www.epa.gov/airmarkets/"
                   "national-electric-energy-data-system-needs-v6\">"
                   "https://www.epa.gov/airmarkets/"
                   "national-electric-energy-data-system-needs-v6</a></p>"
                   f"{pudl_description}",
    "creators": creators,
    "access_right": "open",
    "license": "other-pd",
    "keywords": [
        "epa", "ipm", "needs", "usa", "integrated planning model", epaipm_uuid
    ]
}

# For the census archive.
censusdp1tract_uuid = "beb36017-3fca-49be-a93a-7298f30ca3a3"
censusdp1tract = {
    "title": "PUDL Raw Census DP1 Tract GeoDatabase",
    "language": "eng",
    "upload_type": "dataset",
    "description": "<p>US Census Demographic Profile 1 County and Tract GeoDatabase "
                   "archived from\n"
                   "<a href=\"https://www2.census.gov/geo/tiger/TIGER2010DP1/"
                   "Profile-County_Tract.zip\">"
                   "https://www2.census.gov/geo/tiger/TIGER2010DP1/"
                   "Profile-County_Tract.zip</a></p>"
                   f"{pudl_description}",
    "creators": creators,
    "access_right": "open",
    "license": "other-pd",
    "keywords": [
        "census", "usa", "geodata", "geodatabase", "gis", "spatial", "demographic",
        "dp1", "population", "county", "fips", "tract", censusdp1tract_uuid
    ]
}
