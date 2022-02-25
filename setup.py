#!/usr/bin/env python
"""Archive raw PUDL inputs as frictionless data packages on Zenodo."""

from setuptools import find_packages, setup

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
        "catalystcoop.pudl @ git+https://github.com/catalyst-cooperative/pudl.git@dev",
        "pydantic[email]~=1.7",
        "requests<3",
        "semantic_version<3",
    ],
    extras_require={
        "test": [
            "bandit~=1.6",
            "coverage>=5.3,<7.0",
            "doc8~=0.9",
            "flake8~=4.0",
            "flake8-builtins~=1.5",
            "flake8-colors~=0.1",
            "flake8-docstrings~=1.5",
            "flake8-rst-docstrings~=0.2",
            "flake8-use-fstring~=1.0",
            "mccabe~=0.6",
            "pep8-naming~=0.12",
            "pre-commit~=2.9",
            "pydocstyle>=5.1,<7.0",
            "pytest>=6.2,<8.0",
            "pytest-cov>=2.10,<4.0",
            "tox~=3.20",
        ]
    }
)
