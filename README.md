# PUDL Utils for Zenodo storage and packaging

## zs

The zs.ZenStorage module provides an interface to create archives and upload
files to Zenodo.

## datapackage

The datapackage module provides an OO library for creating frictionless
datapackage metadata, as well as prepared instances appropriate for PUDL
archives.

--

OO Structure

Archive:
    id

    name
    description
    title
    profile
    keywords: [str]
    licences: [license]    
    homepage
    created: datetime
    sources: [source]
    contributors: [contrubitor]
    resources: [resource]


Source:
    title
    path


License:
    name
    title
    path


Contributor:
    title
    path
    role
    organization


Resource:
    name
    profile
    path
    title
    parts: dict
    encoding:
    mediatype:
    format:
    bytes:
    hash:
