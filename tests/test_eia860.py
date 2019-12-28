# -*- coding: utf-8 -*-
import random

from frictionless import eia860

class TestEia860:
    """Ensure we can create proper frictionless datapackage descriptions"""

    def test_single_file(self):
        """Ensure a single file gets a good resource descriptor"""
        year = random.randint(2001, 2020)
        name = "eia860-%d.zip" % year
        size = random.randint(500000, 800000)

        md5_hash = random.choice([
            "7f85506d596de2b5088054ec509b9190",
            "d5f527a0768ddb6e66ef0ff561f0302c",
            "eaaf357571364fea9bfb722dadae3f50"])

        url = random.choice([
            "https://sandbox.zenodo.org/api/deposit/depositions/430193/files/57822118-41e3-49e7-ba15-128139f22338",
            "https://sandbox.zenodo.org/api/deposit/depositions/430193/files/bc8c0768-24c1-4e2e-9b10-276a5b686c41",
            "https://sandbox.zenodo.org/api/deposit/depositions/430193/files/b425e22a-3e84-412a-a29e-f8d87a1fc58a"])

        res = eia860.archive_resource(name, url, size, md5_hash)

        assert(res["name"] == name)
        assert(res["title"] == "eia860-%d" % year)
        assert(res["path"] == url)
        assert(res["parts"]["year"] == year)

        assert(res["mediatype"] == "application/zip")
        assert(res["format"] == "zip")

        assert(res["bytes"] == size)
        assert(res["hash"] == md5_hash)
