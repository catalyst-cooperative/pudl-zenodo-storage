# -*- coding: utf-8 -*-
from faker import Faker
import uuid
import random

from frictionless import ipm_source


class TestIpmSource:
    """Ensure we can create proper frictionless datapackage descriptions"""

    def fake_resource(self, filename):
        """Produce a fake file resource descriptor"""
        fake = Faker()
        md5_hash = fake.md5(raw_output=False)
        size = random.randint(5000, 9999)
        url = "https://zenodo.org/api/deposit/depositions/%d/files/%s" % (
            random.randint(10000, 99999), uuid.uuid4())

        return {
            "filename": filename,
            "links": {"self": url},
            "filesize": size,
            "checksum": md5_hash
            }

    def test_xlsx_file(self):
        """Ensure a single xlsx file gets a good resource descriptor"""
        fake = Faker()
        date = fake.date_between(start_date="-1y", end_date="today")
        name = "ipm-v6-rev-%s.xlsx" % date.isoformat()

        fake_resource = self.fake_resource(name)
        package = ipm_source.datapackager([fake_resource])
        res = package["resources"][0]

        assert res["name"] == name
        assert res["title"] == "ipm-v6-rev-%s" % date.isoformat()
        assert res["parts"]["year"] == date.year
        assert res["parts"]["month"] == date.month
        assert res["parts"]["day"] == date.day

        assert res["path"] == fake_resource["links"]["self"]
        assert(res["mediatype"] == "application/vnd.openxmlformats-"
                                   "officedocument.spreadsheetml.sheet")
        assert res["format"] == "xlsx"

        assert res["bytes"] == fake_resource["filesize"]
        assert res["hash"] == fake_resource["checksum"]

    def test_year_only_file(self):
        """Files with a year and no other date info still get the year"""
        year = random.randint(1990, 2020)
        name = "needs_v6_november_%d_reference_case_%d.xlsx" % (
            year, random.randint(0, 9))

        fake_resource = self.fake_resource(name)
        package = ipm_source.datapackager([fake_resource])
        res = package["resources"][0]

        assert res["name"] == name
        assert res["title"] == name[:-5]
        assert res["parts"] == {"year": year}

        assert res["path"] == fake_resource["links"]["self"]
        assert(res["mediatype"] == "application/vnd.openxmlformats-"
                                   "officedocument.spreadsheetml.sheet")
        assert res["format"] == "xlsx"

        assert res["bytes"] == fake_resource["filesize"]
        assert res["hash"] == fake_resource["checksum"]

    def test_file_sans_parts(self):
        """Files with no year are accepted"""
        name = "epaipm.zip"
        fake_resource = self.fake_resource(name)
        package = ipm_source.datapackager([fake_resource])
        res = package["resources"][0]

        assert res["name"] == name
        assert res["title"] == name[:-4]
        assert res["parts"] is None

        assert res["path"] == fake_resource["links"]["self"]
        assert res["mediatype"] == "application/zip"
        assert res["format"] == "zip"

        assert res["bytes"] == fake_resource["filesize"]
        assert res["hash"] == fake_resource["checksum"]