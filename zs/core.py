# -*- coding: utf-8 -*-

import json
import logging
import requests
import semantic_version


eia860_metadata = {
    "title": "Eia860 Source",
    "upload_type": "dataset",
    "description": "Eia860 Form Data, archived from "
                   "https://www.eia.gov/electricity/data/eia860/",
    "creators": [
        {"name": "Source: US Energy Information Administration"},
        {"name": "Uploaded: Catalyst Cooperative"}
    ],
    "access_right": "open",
    "keywords": ["eia860", "electricity", "usa"]
}


class ZenStorage:
    """Thin interface to store data with zenodo.org via their api"""

    def __init__(self, key, logger=None, testing=False):
        """
        Prepare the ZenStorage interface

        Args:
            key (str): The API key required to authenticate with Zenodo
            testing (bool): If true, use the Zenodo sandbox api rather than the
                production service

        Returns:
            ZenStorage
        """
        if logger is None:
            logger = logging.Logger(__name__)

        self.logger = logger
        self.key = key

        if testing:
            self.api_root = "https://sandbox.zenodo.org/api"
        else:
            self.api_root = "https://zenodo.org/api"

    def get_deposition(self, query):
        """
        Get data for a single Deposition (see developers.zenodo.org) based on
        the provided query.

        Args:
            query (str): A Zenodo (elasticsearch) compatible query string.
                         eg. 'title:"Eia860"' or 'doi:"10.5072/zenodo.415988"'

        Returns:
            - If no such deposition exists, returns None.
            - If a single deposition matches, returns the deposition data as
              dict, per https://developers.zenodo.org/?python#depositions
            - If more than one deposition matches, throws an exception

        """
        url = self.api_root + "/deposit/depositions"
        params = {"q": query, "access_token": self.key}

        lookup = requests.get(url, params)

        jsr = lookup.json()

        if lookup.status_code != 200:
            msg = "Could not look up deposition: %s" % jsr
            self.logger.error(msg)
            raise RuntimeError(msg)

        if len(jsr) > 1:
            msg = "Expected single deposition, query: %s, got: %d" % (
                query, len(jsr))
            self.logger.error(msg)
            raise ValueError(msg)

        if jsr == []:
            return

        return jsr[0]

    def create_deposition(self, metadata):
        """
        Create a deposition resource.  This should only be called once for a
        given data source.  The deposition will be prepared in draft form, so
        that files can be added prior to publication.

        Args:
            metadata: deposition metadata as a dict, per
            https://developers.zenodo.org/?python#representation

        Returns:
            deposition data as dict, per
            https://developers.zenodo.org/?python#depositions
        """
        url = self.api_root + "/deposit/depositions"
        params = {"access_token": self.key}
        headers = {"Content-Type": "application/json"}

        if metadata.get("version", None) is None:
            self.logger.debug("Deposition %s metadata assigned version 1.0.0"
                              % metadata["title"])
            metadata["version"] = "1.0.0"

        data = json.dumps({"metadata": metadata})

        response = requests.post(
            url, params=params, data=data, headers=headers)
        jsr = response.json()

        if response.status_code != 201:
            msg = "Could not create deposition: %s" % jsr
            self.logger.error(msg)
            raise RuntimeError(msg)

        return jsr

    def update_deposition(self, deposition_url, metadata):
        raise NotImplementedError("Not ready yet.")

    def new_deposition_version(self, conceptdoi, version_info=None):
        """
        Produce a new version for a given deposition archive

        Args:
            conceptdoi: deposition conceptdoi, per
                        https://help.zenodo.org/#versioning

                        The deposition provided must already exist on Zenodo.

            version_info: a semantic_version.Version.  By default the version metadata
                will be incremented by on major semantic version number

        Returns:
            deposition data as dict, per
            https://developers.zenodo.org/?python#depositions
        """
        query = 'conceptdoi:"%s"' % conceptdoi
        deposition = self.get_deposition(query)

        if deposition is None:
            raise ValueError("Deposition '%s' does not exist" % query)

        if deposition["state"] == "unsubmitted":
            self.logger.debug("deposition '%s' is already a new version" %
                              deposition["id"])
            return deposition

        url = self.api_root + "/deposit/depositions/%d/actions/newversion" \
            % deposition["id"]

        # Create the new version
        params = {"access_token": self.key}
        response = requests.post(url, params=params)
        jsr = response.json()

        if response.status_code != 201:
            msg = "Could not create new version: %s" % jsr
            self.logger.error(msg)
            raise RuntimeError(msg)

        # When the API creates a new version, it does not return the new one.
        # It returns the old one with a link to the new one.
        metadata = jsr["metadata"]

        if version_info is None:
            previous = semantic_version.Version(metadata["version"])
            version_info = previous.next_major()

        metadata["version"] = str(version_info)

        new_version = self.get_deposition('conceptdoi:"%s"' % conceptdoi)
        return self.update_deposition(new_version, metadata)

    def file_api_upload(self, deposition, file_name, file_handle):
        """
        Upload a file for the given deposition, using the older file api

        Args:
            deposition: the dict of the deposition resource
            file_name: the desired file name
            file_handle: an open file handle or bytes like object.
                Must be < 100MB

        Returns:
            dict of the deposition file resource, per
                https://developers.zenodo.org/#deposition-files
        """
        url = deposition["links"]["files"]
        data = {"name": file_name, "access_token": self.key}
        files = {"file": file_handle}
        response = requests.post(url, data=data, files=files)
        jsr = response.json()

        if response.status_code != 201:
            msg = "Failed to upload file: %s" % jsr
            self.logger.error(msg)
            raise RuntimeError(msg)

        return jsr

    def bucket_api_upload(self, deposition, file_name, file_handle):
        """
        Upload a file for the given deposition, using the newer bucket api

        Args:
            deposition: the dict of the deposition resource
            file_name: the desired file name
            file_handle: an open file handle or bytes like object.
                Must be < 100MB

        Returns:
            dict of the deposition file resource, per
                https://developers.zenodo.org/#deposition-files
        """
        url = deposition["links"]["bucket"] + "/" + file_name
        params = {"access_token": self.key}
        response = requests.put(url, params=params, data=file_handle)
        jsr = response.json()

        if response.status_code not in [200, 201]:
            msg = "Failed to upload file: code %d / %s on %s" % \
                (response.status_code, jsr, deposition)
            self.logger.error(msg)
            raise RuntimeError(msg)

        return jsr
