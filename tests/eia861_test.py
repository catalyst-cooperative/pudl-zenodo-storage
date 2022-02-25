"""Tests for the EIA-861."""
import random

from datapackage import Package
from faker import Faker

from frictionless import eia861


class TestEia861:
    """Ensure we can create proper frictionless datapackage descriptions."""

    def test_single_file(self, zenodo_url):
        """Ensure a single file gets a good resource descriptor."""
        fake = Faker()
        year = random.randint(1990, 2019)
        name = f"eia861-{year}.zip"
        size = random.randint(500000, 800000)

        md5_hash = fake.md5(raw_output=False)
        url = zenodo_url

        fake_resource = {
            "filename": name,
            "links": {"download": url},
            "filesize": size,
            "checksum": md5_hash
        }

        package = eia861.datapackager([fake_resource])
        res = package["resources"][0]

        assert(Package(descriptor=package).valid)
        assert(res["name"] == name)
        assert(res["title"] == f"eia861-{year}")
        assert(res["path"] == url)
        assert(res["parts"]["year"] == year)
        assert(res["remote_url"] == url)

        assert(res["mediatype"] == "application/zip")
        assert(res["format"] == "zip")

        assert(res["bytes"] == size)
        assert(res["hash"] == md5_hash)
