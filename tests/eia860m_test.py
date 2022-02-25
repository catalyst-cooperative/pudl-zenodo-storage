"""Tests for EIA 860M."""
import random

from datapackage import Package
from faker import Faker

from frictionless import eia860m


class TestEia860M:
    """Ensure we can create proper frictionless datapackage descriptions."""

    def test_single_file(self, zenodo_url):
        """Ensure a single file gets a good resource descriptor."""
        fake = Faker()
        year = random.randint(2016, 2019)
        month = str(random.randint(1, 12)).zfill(2)
        name = f"eia860m-{year}-{month}.xlsx"
        size = random.randint(500000, 800000)

        md5_hash = fake.md5()

        url = zenodo_url

        fake_resource = {
            "filename": name,
            "links": {"download": url},
            "filesize": size,
            "checksum": md5_hash,
        }

        package = eia860m.datapackager([fake_resource])
        res = package["resources"][0]

        assert Package(descriptor=package).valid
        assert res["name"] == name
        assert res["title"] == f"eia860m-{year}-{month}"
        assert res["path"] == url
        assert res["parts"]["year_month"] == f"{year}-{month}"
        assert res["remote_url"] == url

        assert (
            res["mediatype"]
            == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        assert res["format"] == "xlsx"

        assert res["bytes"] == size
        assert res["hash"] == md5_hash
