from faker import Faker
import uuid
import random

from frictionless import epaipm_raw


class TestIpmSource:
    """Ensure we can create proper frictionless datapackage descriptions."""

    def fake_resource(self, filename):
        """Produce a fake file resource descriptor."""
        fake = Faker()
        md5_hash = fake.md5(raw_output=False)
        size = random.randint(5000, 9999)
        url = "https://zenodo.org/api/deposit/depositions/%d/files/%s" % (
            random.randint(10000, 99999), uuid.uuid4())

        return {
            "filename": filename,
            "links": {"download": url},
            "filesize": size,
            "checksum": md5_hash
        }

    def test_xlsx_file(self):
        """Ensure a single xlsx file gets a good resource descriptor."""
        fake = Faker()
        date = fake.date_between(start_date="-1y", end_date="today")
        name = "epaipm-v6-rev-%s.xlsx" % date.isoformat()

        fake_resource = self.fake_resource(name)
        package = epaipm_raw.datapackager([fake_resource])
        res = package["resources"][0]

        assert res["name"] == name
        assert res["title"] == "epaipm-v6-rev-%s" % date.isoformat()
        assert res["parts"]["year"] == date.year
        assert res["parts"]["month"] == date.month
        assert res["parts"]["day"] == date.day

        assert res["path"] == fake_resource["links"]["download"]
        assert(res["mediatype"] == "application/vnd.openxmlformats-"
                                   "officedocument.spreadsheetml.sheet")
        assert res["format"] == "xlsx"

        assert res["bytes"] == fake_resource["filesize"]
        assert res["hash"] == fake_resource["checksum"]

    def test_year_only_file(self):
        """Files with a year and no other date info still get the year."""
        year = random.randint(1990, 2020)
        name = "table_3-%d_annual_transmission_capabilities_of_u.s._" \
               "model_regions_in_epa_platform_v6_-_%d.xlsx" % (
                   random.randint(1, 99), year)
        print(name)

        fake_resource = self.fake_resource(name)
        package = epaipm_raw.datapackager([fake_resource])
        res = package["resources"][0]

        assert res["name"] == name
        assert res["title"] == name[:-5]
        assert res["parts"]["year"] == year

        assert res["path"] == fake_resource["links"]["download"]
        assert res["remote_url"] == fake_resource["links"]["download"]
        assert(res["mediatype"] == "application/vnd.openxmlformats-"
                                   "officedocument.spreadsheetml.sheet")
        assert res["format"] == "xlsx"

        assert res["bytes"] == fake_resource["filesize"]
        assert res["hash"] == fake_resource["checksum"]

    def test_file_sans_parts(self):
        """Files with no year are accepted."""
        name = "epaipm.zip"
        fake_resource = self.fake_resource(name)
        package = epaipm_raw.datapackager([fake_resource])
        res = package["resources"][0]

        assert res["name"] == name
        assert res["title"] == name[:-4]
        assert res["remote_url"] == fake_resource["links"]["download"]

        assert res["path"] == fake_resource["links"]["download"]
        assert res["mediatype"] == "application/zip"
        assert res["format"] == "zip"

        assert res["bytes"] == fake_resource["filesize"]
        assert res["hash"] == fake_resource["checksum"]
