import uuid
import random
from datapackage import Package

from frictionless import eia860


class TestEia860:
    """Ensure we can create proper frictionless datapackage descriptions."""

    def test_single_file(self):
        """Ensure a single file gets a good resource descriptor."""
        year = random.randint(2001, 2020)
        name = "eia860-%d.zip" % year
        size = random.randint(500000, 800000)

        md5_hash = random.choice([
            "7f85506d596de2b5088054ec509b9190",
            "d5f527a0768ddb6e66ef0ff561f0302c",
            "eaaf357571364fea9bfb722dadae3f50"])

        url = "https://zenodo.org/api/deposit/depositions/%d/files/%s" % (
            random.randint(10000, 99999), uuid.uuid4())

        fake_resource = {
            "filename": name,
            "links": {"download": url},
            "filesize": size,
            "checksum": md5_hash
        }

        package = eia860.datapackager([fake_resource])
        res = package["resources"][0]

        assert(Package(descriptor=package).valid)
        assert(res["name"] == name)
        assert(res["title"] == "eia860-%d" % year)
        assert(res["path"] == url)
        assert(res["parts"]["year"] == year)
        assert(res["remote_url"] == url)

        assert(res["mediatype"] == "application/zip")
        assert(res["format"] == "zip")

        assert(res["bytes"] == size)
        assert(res["hash"] == md5_hash)
