# -*- coding: utf-8 -*-

import uuid
import random
from frictionless import ferc714_source


class TestFerc714Source:
    """Ensure we can create proper frictionless datapackage descriptions."""

    def test_file_resource(self):
        """Test that file resources are made correctly."""
        name = random.choice(["form714.zip", "ferc714.zip"])
        url = "https://zenodo.org/api/deposit/depositions/%d/files/%s" % (
            random.randint(10000, 99999), uuid.uuid4())
        size = random.randint(500000, 800000)
        md5_hash = random.choice([
            "76702bc3ebd6b21f34a11e4eeeffc76b",
            "aeea7b3db681046e247de438314f572b",
            "b7a0d6db9e9db4eb4beab2103f020065"])

        fake_resource = {
            "filename": name,
            "links": {"download": url},
            "filesize": size,
            "checksum": md5_hash
        }

        package = ferc714_source.datapackager([fake_resource])
        res = package["resources"][0]

        assert(res["name"] == name)
        assert(res["title"] == name[:-4])
        assert(res["path"] == url)
        assert(res["parts"]["remote_url"] == url)

        assert(res["mediatype"] == "application/zip")
        assert(res["format"] == "zip")

        assert(res["bytes"] == size)
        assert(res["hash"] == md5_hash)
