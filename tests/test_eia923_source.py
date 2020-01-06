# -*- coding: utf-8 -*-
import uuid
import random

from frictionless import eia923_source


class TestEia923Source:
    """Ensure we can create proper frictionless datapackage descriptions"""

    def test_single_file_resource(self):
        """Ensure a single file gets a good resource descriptor"""

        year = random.randint(2001, 2020)
        name = "eia923-%d.zip" % year
        size = random.randint(500000, 800000)

        md5_hash = random.choice([
            "4bd7e1025c91c00b50b6cef87cb9bfad",
            "883895453cb3144b97d0095472f6136e",
            "c271dfc0ca452b6582f0e592f57351ef"])

        url = "https://zenodo.org/api/deposit/depositions/%d/files/%s" % (
            random.randint(10000, 99999), uuid.uuid4())

        fake_resource = {
            "filename": name,
            "links": {"self": url},
            "filesize": size,
            "checksum": md5_hash
            }

        package = eia923_source.datapackager([fake_resource])
        res = package["resources"][0]

        assert(res["name"] == name)
        assert(res["title"] == "eia923-%d" % year)
        assert(res["path"] == url)
        assert(res["parts"]["year"] == year)

        assert(res["mediatype"] == "application/zip")
        assert(res["format"] == "zip")

        assert(res["bytes"] == size)
        assert(res["hash"] == md5_hash)
