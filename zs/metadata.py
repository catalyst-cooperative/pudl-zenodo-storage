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
This archive contains raw input data for the Public Utility Data Liberation (PUDL)
software developed by Catalyst Cooperative. It is organized into programmatically usable
Frictionless Data Packages. For additional information on how to use this data see:

    https://github.com/catalyst-cooperative/pudl
    https://readthedocs.org/projects/catalystcoop-pudl/
    https://zenodo.org/communities/catalyst-cooperative/
    https://specs.frictionlessdata.io/data-package/
    https://catalyst.coop

"""

# Unaltered Eia860 archive.
eia860_source_uuid = "a93cdabd-706f-48c7-ae02-4463dacf1419"
eia860_source = {
    "title": "PUDL Raw EIA Form 860",
    "language": "eng",
    "upload_type": "dataset",
    "description": "Raw US Energy Information Administration (EIA) Form 860 data, "
                   "archived from "
                   "https://www.eia.gov/electricity/data/eia860/"
                   f"{pudl_description}",
    "creators": creators,
    "access_right": "open",
    "keywords": [
        "electricity", "electric", "boiler", "generator", "plant", "utility",
        "fuel", "coal", "natural gas", " prime mover", "eia860", "retirement",
        "capacity", "planned", "proposed", "energy", "hydro", "solar", "wind",
        "nuclear", "form 860", "eia", "annual", "gas", "ownership", "steam",
        "turbine", "combustion", "combined cycle", "eia",
        "energy information administration", "usa", eia860_source_uuid]
}


# Unaltered Eia861 archive.
eia861_source_uuid = "70999ef2-50e9-47ae-a4f6-5d69e6ff98d1"
eia861_source = {
    "title": "PUDL Raw EIA Form 861",
    "language": "eng",
    "upload_type": "dataset",
    "description": "Raw US Energy Information Administration (EIA) Form 861 Data, "
                   "archived from "
                   "https://www.eia.gov/electricity/data/eia861/"
                   f"{pudl_description}",
    "creators": creators,
    "access_right": "open",
    "keywords": [
        "electricity", "electric", "boiler", "generator", "plant", "utility",
        "fuel", "coal", "natural gas", " prime mover", "eia861", "retirement",
        "capacity", "planned", "proposed", "energy", "hydro", "solar", "wind",
        "nuclear", "form 861", "eia", "annual", "gas", "ownership", "steam",
        "turbine", "combustion", "combined cycle", "eia",
        "energy information administration", "usa", eia861_source_uuid]
}


# Unaltered Eia923 archive.
eia923_source_uuid = "53831f63-fa82-475a-bef4-5b5f0b7c41a4"
eia923_source = {
    "title": "PUDL Raw EIA Form 923",
    "language": "eng",
    "upload_type": "dataset",
    "description": "Raw US Energy Information Administration (EIA) Form 923 data, "
                   "archived from "
                   "https://www.eia.gov/electricity/data/eia923/"
                   f"{pudl_description}",
    "creators": creators,
    "access_right": "open",
    "keywords": [
        "fuel", "boiler", "generator", "plant", "utility", "cost", "price",
        "natural gas", "coal", "eia923", "energy", "electricity", "form 923",
        "receipts", "generation", "net generation", "monthly", "annual", "gas",
        "fuel consumption", "MWh", "energy information administration", "eia",
        "mercury", "sulfur", "ash", "lignite", "bituminous", "subbituminous",
        "heat content", eia923_source_uuid]
}


# Unaltered EPA CEMS archive
epacems_source_uuid = "8bd99e7d-b11a-4bd1-8af0-bccf984dcc43"
epacems_source = {
    "title": "PUDL Raw EPA CEMS Hourly",
    "language": "eng",
    "upload_type": "dataset",
    "description": "Raw US EPA hourly Continuous Emissions Monitoring System "
                   "(CEMS) data, archived from "
                   "ftp://newftp.epa.gov/dmdnload/emissions/hourly/monthly"
                   f"{pudl_description}",
    "creators": creators,
    "access_right": "open",
    "keywords": [
        "epa", "us", "emissions", "pollution", "ghg", "so2", "co2", "sox",
        "nox", "load", "utility", "electricity", "plant", "generator", "unit",
        "generation", "capacity", "output", "power", "heat content", "mmbtu",
        "steam", "cems", "continuous emissions monitoring system", "hourly"
        "environmental protection agency", "ampd", "air markets program data",
        epacems_source_uuid]
}

# For the unaltered Ferc1 archive.
ferc1_source_uuid = "d3d91c87-c595-49d5-a7f3-e5f5669c8306"
ferc1_source = {
    "title": "PUDL Raw FERC Form 1",
    "language": "eng",
    "upload_type": "dataset",
    "description": "Raw Federal Energy Regulatory Commission (FERC) Form 1 data, "
                   "archived from "
                   "https://www.ferc.gov/industries-data/electric/"
                   "general-information/electric-industry-forms/"
                   "form-1-electric-utility-annual",
    "creators": creators,
    "access_right": "open",
    "keywords": [
        "electricity", "electric", "utility", "plant", "steam", "generation",
        "cost", "expense", "price", "heat content", "ferc", "form 1",
        "federal energy regulatory commission", "capital", "accounting",
        "depreciation", "finance", "plant in service", "hydro", "coal",
        "natural gas", "gas", "opex", "capex", "accounts", "investment",
        "capacity", "usa", ferc1_source_uuid]
}

# Unaltered Ferc714 archive.
ferc714_source_uuid = "f31f0894-639e-4bc2-9b7f-8a84713bcc87"
ferc714_source = {
    "title": "PUDL Raw FERC Form 714",
    "language": "eng",
    "upload_type": "dataset",
    "description": "Federal Energy Regulatory Commission (FERC) Form 714 Data, "
                   "archived from "
                   "https://www.ferc.gov/industries-data/electric/"
                   "general-information/electric-industry-forms/"
                   "form-no-714-annual-electric/data"
                   f"{pudl_description}",
    "creators": creators,
    "keywords": [
        "electricity", "electric", "utility", "plant", "steam", "generation",
        "cost", "expense", "price", "heat content", "ferc", "form 714",
        "federal energy regulatory commission", "capital", "accounting",
        "depreciation", "finance", "plant in service", "hydro", "coal",
        "natural gas", "gas", "opex", "capex", "accounts", "investment",
        "capacity", "usa", ferc714_source_uuid]
}

# For the unaltered IPM archive.
epaipm_source_uuid = "75b29994-bd39-4518-a5b2-ec180a18ac23"
epaipm_source = {
    "title": "PUDL Raw EPA IPM/NEEDS",
    "language": "eng",
    "upload_type": "dataset",
    "description": "Select data pertaining to the US EPA Integrated Planning Model / "
                   "National Electric Energy Data System (IPM/NEEDS) "
                   "Archived from "
                   "https://www.epa.gov/airmarkets/"
                   "national-electric-energy-data-system-needs-v6"
                   f"{pudl_description}",
    "creators": creators,
    "access_right": "open",
    "keywords": ["epa", "ipm", "needs", "usa", "integrated planning",
                 epaipm_source_uuid],
}

# For the census archive.
censusdp1tract_source_uuid = "beb36017-3fca-49be-a93a-7298f30ca3a3"
censusdp1tract_source = {
    "title": "PUDL Raw Census DP1 Tract GeoDatabase",
    "language": "eng",
    "upload_type": "dataset",
    "description": "US Census Demographic Profile 1 County and Tract GeoDatabase "
                   "archived from "
                   "https://www2.census.gov/geo/tiger/TIGER2010DP1/"
                   "Profile-County_Tract.zip"
                   f"{pudl_description}",
    "creators": creators,
    "access_right": "open",
    "keywords": [
        "census", "usa", "geodata", "geodatabase", "gis", "spatial", "demographic",
        "dp1", "population", "county", "fips", "tract", censusdp1tract_source_uuid
    ]
}
