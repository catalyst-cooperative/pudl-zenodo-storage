import uuid
import random

from frictionless import eia861_source


class TestEia861:
    """Ensure we can create proper frictionless datapackage descriptions"""

    def test_single_file(self):
        """Ensure a single file gets a good resource descriptor"""

        year = random.randint(2001, 2019)
        name = "eia861-%d.zip" % year
        size = random.randint(500000, 800000)

        md5_hash = random.choice([
            "48d28163ced6add3ed324a641bed077b",
            "028a5fa8c5d302a9817960a155c93570",
            "d2956f209926175c219571f47281b1e8"])

        url = "https://zenodo.org/api/deposit/depositions/%d/files/%s" % (
            random.randint(10000, 99999), uuid.uuid4())

        fake_resource = {
            "filename": name,
            "links": {"self": url},
            "filesize": size,
            "checksum": md5_hash
            }

        package = eia861_source.datapackager([fake_resource])
        res = package["resources"][0]

        assert(res["name"] == name)
        assert(res["title"] == "eia861-%d" % year)
        assert(res["path"] == url)
        assert(res["parts"]["year"] == year)

        assert(res["mediatype"] == "application/zip")
        assert(res["format"] == "zip")

        assert(res["bytes"] == size)
        assert(res["hash"] == md5_hash)
