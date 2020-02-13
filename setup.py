#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="ZenTools",
    version="0.2.0",
    packages=find_packages(),
    author="Catalyst Cooperative",
    description="Zenodo storage interface and scripts",
    scripts=["./bin/zen_store.py"]
    )
