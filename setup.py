#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="pudl_zenodo_storage",
    version="0.2.0",
    packages=find_packages(),
    author="Catalyst Cooperative",
    description="Zenodo storage interface and scripts",
    scripts=["./bin/zenodo_store.py"]
)
