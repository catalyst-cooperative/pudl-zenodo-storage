import uuid
import random
from frictionless import censusdp1tract


class TestCensusDp1TractSource:
    """Ensure we can create proper frictionless datapackage descriptions."""

    def test_file_resource(self):
        """Test that file resources are made correctly."""
        name = "censusdp1tract-2010.zip"
        url = "https://zenodo.org/api/deposit/depositions/%d/files/%s" % (
            random.randint(10000, 99999), uuid.uuid4())
        size = random.randint(500000, 800000)
        md5_hash = random.choice([
            "a07e61999fff9ba2cd240bfb874db45e",
            "6a45164181cef4f86fab24dd2c4fa9a2",
            "4dd146387c256d4424ebc94ed2976d0c"])

        fake_resource = {
            "filename": name,
            "links": {"download": url},
            "filesize": size,
            "checksum": md5_hash
        }

        package = censusdp1tract.datapackager([fake_resource])
        res = package["resources"][0]

        assert(res["name"] == name)
        assert(res["title"] == name[:-4])
        assert(res["path"] == url)
        assert(res["remote_url"] == url)

        assert(res["mediatype"] == "application/zip")
        assert(res["format"] == "zip")

        assert(res["bytes"] == size)
        assert(res["hash"] == md5_hash)
