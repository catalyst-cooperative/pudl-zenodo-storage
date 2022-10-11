#!/usr/bin/env python
"""Archive raw PUDL inputs as frictionless data packages on Zenodo."""

from setuptools import find_packages, setup

setup(
    name="pudl_zenodo_storage",
    version="0.2.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    author="Catalyst Cooperative",
    description="Zenodo storage interface and scripts",
    python_requires=">=3.10,<3.11",
    entry_points={
        "console_scripts": [
            "zenodo_store = pudl_zenodo_storage.cli:main",
        ]
    },
    license="MIT",
    install_requires=[
        "catalystcoop.pudl @ git+https://github.com/catalyst-cooperative/pudl.git@dev",
        "datapackage>=1.0,<2.0",
        "factory_boy>=2.12,<4",
        "pydantic[email]>=1.7,<2",
        "requests>=2.22,<3",
        "semantic_version>=2.8,<3",
    ],
    extras_require={
        "test": [
            "bandit>=1.6,<2",
            "black>=22,<23",
            "coverage>=5.3,<6.6",
            "doc8>=0.9,<1.1",
            "flake8>=4.0,<5.1",
            "flake8-builtins>=1.5,<3",
            "flake8-colors~=0.1",
            "flake8-docstrings>=1.5,<2",
            "flake8-rst-docstrings~=0.2",
            "flake8-use-fstring>=1.0,<2",
            "mccabe~=0.6",
            "pep8-naming~=0.12",
            "pre-commit>=2.9,<3",
            "pydocstyle>=5.1,<7",
            "pytest>=6.2,<8",
            "pytest-cov>=2.10,<5",
            "tox>=3.20,<4",
        ]
    },
)
