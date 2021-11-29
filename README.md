# PUDL Utils for Zenodo storage and packaging

# Installation

We recommend using conda to create and manage your environment.

Run:
```
conda env create -f environment.yml
conda activate pudl-zenodo-storage
```

## zs

The zs.ZenodoStorage class provides an interface to create archives and upload
files to Zenodo.

## frictionless

Package metadata in dict formats, as necessary to support the frictionless
(datapackage
library)[https://frictionlessdata.io/docs/using-data-packages-in-python/]
specification.
