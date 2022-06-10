"""Tests for EPA CEMS unitid to EIA plant Crosswalk file."""
import random

from datapackage import Package
from faker import Faker

from pudl_zenodo_storage.frictionless import epacems_unitid_eia_plant_crosswalk


class TestEpaEiaCrosswalkSource:
    """Ensure we can create proper frictionless datapackage descriptions."""

    def test_file_resource(self, zenodo_url):
        """Test that file resources are made correctly."""
        fake = Faker()
        name = "epacems_unitid_eia_plant_crosswalk.zip"
        url = zenodo_url
        size = random.randint(500000, 800000)
        md5_hash = fake.md5(raw_output=False)

        fake_resource = {
            "filename": name,
            "links": {"download": url},
            "filesize": size,
            "checksum": md5_hash,
        }

        package = epacems_unitid_eia_plant_crosswalk.datapackager([fake_resource])
        res = package["resources"][0]
        print(Package(descriptor=package).errors)

        assert Package(descriptor=package).valid
        assert res["name"] == name
        assert res["title"] == name[:-4]
        assert res["path"] == url
        assert res["remote_url"] == url

        assert res["mediatype"] == "application/zip"
        assert res["format"] == "zip"

        assert res["bytes"] == size
        assert res["hash"] == md5_hash
