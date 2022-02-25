"""Tests for archiving the Raw EIA 860 data."""
import random

from datapackage import Package
from faker import Faker

from frictionless import eia860


class TestEia860:
    """Ensure we can create proper frictionless datapackage descriptions."""

    def test_single_file(self, zenodo_url):
        """Ensure a single file gets a good resource descriptor."""
        fake = Faker()
        year = random.randint(2001, 2020)
        name = f"eia860-{year}.zip"
        size = random.randint(500000, 800000)

        md5_hash = fake.md5(raw_output=False)

        url = zenodo_url

        fake_resource = {
            "filename": name,
            "links": {"download": url},
            "filesize": size,
            "checksum": md5_hash,
        }

        package = eia860.datapackager([fake_resource])
        res = package["resources"][0]

        assert Package(descriptor=package).valid
        assert res["name"] == name
        assert res["title"] == f"eia860-{year}"
        assert res["path"] == url
        assert res["parts"]["year"] == year
        assert res["remote_url"] == url

        assert res["mediatype"] == "application/zip"
        assert res["format"] == "zip"

        assert res["bytes"] == size
        assert res["hash"] == md5_hash
