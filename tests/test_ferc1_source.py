# -*- coding: utf-8 -*-
import uuid
import random

from frictionless import ferc1_source


class TestFerc1Source:
    """Ensure we can create proper frictionless datapackage descriptions"""

    def test_single_file_resource(self):
        """Ensure a single file gets a good resource descriptor"""

        year = random.randint(1997, 2020)
        name = "ferc1-%d.zip" % year
        size = random.randint(500000, 800000)

        md5_hash = random.choice([
            "3122e77806b1a1fb2c8af8d404457fd7",
            "d7292a7175af8c08b12594e21de3af1f",
            "01c58b5a83dd55ec1fc46f34065b30e6"])

        url = "https://zenodo.org/api/deposit/depositions/%d/files/%s" % (
            random.randint(10000, 99999), uuid.uuid4())

        fake_resource = {
            "filename": name,
            "links": {"self": url},
            "filesize": size,
            "checksum": md5_hash
            }

        package = ferc1_source.datapackager([fake_resource])
        res = package["resources"][0]

        assert(res["name"] == name)
        assert(res["title"] == "ferc1-%d" % year)
        assert(res["path"] == url)
        assert(res["parts"]["year"] == year)

        assert(res["mediatype"] == "application/zip")
        assert(res["format"] == "zip")

        assert(res["bytes"] == size)
        assert(res["hash"] == md5_hash)
