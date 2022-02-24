#!/usr/bin/env python
"""Archive raw PUDL inputs as frictionless data packages on Zenodo."""

from setuptools import setup, find_packages

setup(
    name="pudl_zenodo_storage",
    version="0.2.0",
    packages=find_packages(),
    author="Catalyst Cooperative",
    description="Zenodo storage interface and scripts",
    scripts=["./bin/zenodo_store.py"],
    python_requires=">=3.8,<3.11",
    license="MIT",
    install_requires=[
        "datapackage<2",
        "factory_boy<3",
        "requests<3",
        "semantic_version<3",
    ],
    extras_require={
        "test": [
            "pytest>=7",
        ]
    }
)
