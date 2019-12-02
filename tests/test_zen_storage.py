# -*- coding: utf-8 -*-
import json
import copy
import io
import os
import random
import requests
import semantic_version

from zs import ZenStorage


class TestZenStorage:
    """
    Ensure that we are able to use the Zenodo service, via sandbox. Integration
    test, accesses extertal resources.
    """

    zs = ZenStorage(key=os.environ["ZENODO_TEST_KEY"], testing=True)
    test_deposition = {
        "title": "PUDL Test",
        "upload_type": "dataset",
        "description": "Test dataset for the sandbox.  Thanks!",
        "creators": [{"name": "Catalyst Cooperative"}],
        "access_right": "open",
        "keywords": ["catalyst", "test", "cooperative"]
    }

    def test_lookup_and_create(self):
        """Ensure lookup and create processes work."""
        td = copy.deepcopy(self.test_deposition)
        td["title"] += ": %d" % random.randint(1000, 9999)

        lookup = self.zs.get_deposition('title:"%s"' % td["title"])
        assert(lookup is None)

        create = self.zs.create_deposition(td)

        for key, _ in td.items():
            assert(create["metadata"][key] == td[key])

        requests.post(
            create["links"]["publish"], data={"access_token": self.zs.key})

        lookup = self.zs.get_deposition('title:"%s"' % td["title"])
        assert(lookup["metadata"]["title"] == td["title"])

    def test_new_version_and_file_api_upload(self):
        """Ensure we can create new versions of a deposition"""
        # It would be better if we could test a single function at a time,
        # however the api does not support versioning without a file upload.
        td = copy.deepcopy(self.test_deposition)
        td["title"] += ": %d" % random.randint(1000, 9999)

        first = self.zs.create_deposition(td)
        fake_file = io.BytesIO(b"This is a test, via the file api.")
        self.zs.file_api_upload(first, "testing.txt", fake_file)

        response = requests.post(first["links"]["publish"],
                                 data={"access_token": self.zs.key})
        published = response.json()

        if response.status_code > 299:
            raise AssertionError(
                "Failed to save test deposition: code %d, %s" %
                (response.status_code, published))

        assert published["state"] == "done"
        assert published["submitted"]

        new_version = self.zs.new_deposition_version(published["conceptdoi"])

        msg = json.dumps([published, new_version], indent=4, sort_keys=True)
        print(msg)

        assert new_version["title"] == first["title"]
        assert new_version["state"] == "unsubmitted"
        assert not new_version["submitted"]

        assert semantic_version.Version(published["metadata"]["version"]) < \
               semantic_version.Version(new_version["metadata"]["version"])

    def test_bucket_api_upload(self):
        """Verify the bucket api upload"""
        td = copy.deepcopy(self.test_deposition)
        td["title"] += ": %d" % random.randint(1000, 9999)

        deposition = self.zs.create_deposition(td)
        fake_file = io.BytesIO(b"This is a test, via the bucket api.")
        self.zs.bucket_api_upload(deposition, "testing.txt", fake_file)
        response = requests.post(deposition["links"]["publish"],
                                 data={"access_token": self.zs.key})
        published = response.json()

        if response.status_code > 299:
            raise AssertionError(
                "Failed to save test deposition: code %d, %s" %
                (response.status_code, published))

        lookup = self.zs.get_deposition('title:"%s"' % td["title"])
        assert lookup["files"][0]["filename"] == "testing.txt"
