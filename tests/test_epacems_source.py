# -*- coding: utf-8 -*-
from faker import Faker
import uuid
import random

from frictionless import epacems_source


class TestIpmSource:
    """Ensure we can create proper frictionless datapackage descriptions"""

    def test_single_file(self):
        """Ensure a single file gets a good resource descriptor"""
        fake = Faker()
        date = fake.date_between(start_date="-10y", end_date="today")
        state = fake.state_abbr(include_territories=False).lower()

        name = "%d%s%02d.zip" % (date.year, state, date.month)
        size = random.randint(500000, 800000)
        md5_hash = fake.md5(raw_output=False)

        url = "https://zenodo.org/api/deposit/depositions/%d/files/%s" % (
            random.randint(10000, 99999), uuid.uuid4())

        fake_resource = {
            "filename": name,
            "links": {"self": url},
            "filesize": size,
            "checksum": md5_hash
            }

        package = epacems_source.datapackager([fake_resource])
        res = package["resources"][0]

        assert(res["name"] == name)
        assert(res["title"] == name[:-4])
        assert(res["path"] == url)
        assert(res["parts"]["year"] == date.year)
        assert(res["parts"]["month"] == date.month)
        assert(res["parts"]["state"] == state)

        assert(res["mediatype"] == "application/zip")
        assert(res["format"] == "zip")

        assert(res["bytes"] == size)
        assert(res["hash"] == md5_hash)
