"""Core routines for archiving raw data packages on Zenodo."""
import json
import logging

import requests
import semantic_version


class ZenodoStorage:
    """Thin interface to store data with zenodo.org via their API."""

    def __init__(self, key, testing=False, verbose=False, loglevel="WARNING"):
        """
        Prepare the ZenodoStorage interface.

        Args:
            key (str): The API key required to authenticate with Zenodo
            testing (bool): If true, use the Zenodo sandbox api rather than the
                production service

        Returns:
            ZenodoStorage

        """
        logger = logging.Logger(__name__)
        logger.setLevel(loglevel)

        if verbose:
            logger.addHandler(logging.StreamHandler())

        self.logger = logger
        self.key = key

        if testing:
            self.api_root = "https://sandbox.zenodo.org/api"
        else:
            self.api_root = "https://zenodo.org/api"

    def get_deposition(self, query):
        """
        Get data for a single Zenodo Deposition based on the provided query.

        See https://developers.zenodo.org for more information.

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
            msg = f"Could not look up deposition: {jsr}"
            self.logger.error(msg)
            raise RuntimeError(msg)

        self.logger.info(jsr)

        if len(jsr) > 1:
            msg = f"Expected single deposition, query: {query}, got: {len(jsr)}"
            self.logger.error(msg)
            raise ValueError(msg)

        if jsr == []:
            return

        return jsr[0]

    def create_deposition(self, metadata):
        """
        Create a Zenodo deposition resource.

        This should only be called once for a given data source.  The deposition will be
        prepared in draft form, so that files can be added prior to publication.

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
            self.logger.debug(
                f"Deposition {metadata['title']} metadata assigned version 1.0.0"
            )
            metadata["version"] = "1.0.0"

        data = json.dumps({"metadata": metadata})

        response = requests.post(url, params=params, data=data, headers=headers)
        jsr = response.json()

        if response.status_code != 201:
            msg = f"Could not create deposition: {jsr}"
            self.logger.error(msg)
            raise RuntimeError(msg)

        return jsr

    def update_deposition(self, deposition_url, metadata):
        """
        Update the metadata of an existing Deposition.

        Args:
            deposition_url: str, url for the deposition, as found in
                deposition["links"]["self"]

            metadata: dict, carrying the replacement metadata

        Returns:
            updated deposition data
        """
        data = json.dumps({"metadata": metadata})
        params = {"access_token": self.key}
        headers = {"Content-Type": "application/json"}

        response = requests.put(
            deposition_url, params=params, data=data, headers=headers
        )
        jsr = response.json()

        if response.status_code != 200:
            msg = f"Failed to update: {jsr} / {json.dumps(metadata)}"
            self.logger.error(msg)
            raise RuntimeError(msg)

        return jsr

    def new_deposition_version(self, conceptdoi, version_info=None):
        """
        Produce a new version for a given deposition archive.

        Args:
            conceptdoi (str): deposition conceptdoi, per
                https://help.zenodo.org/#versioning
                The deposition provided must already exist on Zenodo.
            version_info (semantic_version.Version): By default the version metadata
                will be incremented by on major semantic version number.

        Returns:
            deposition data as dict, per
            https://developers.zenodo.org/?python#depositions

        """
        query = f'conceptdoi:"{conceptdoi}"'
        deposition = self.get_deposition(query)

        if deposition is None:
            raise ValueError(f"Deposition '{query}' does not exist")

        self.logger.debug(
            f"Deposition '{query}' found at {deposition['links']['self']}"
        )

        if deposition["state"] == "unsubmitted":
            self.logger.debug(
                f"deposition '{deposition['id']}' is already a new version"
            )
            return deposition

        url = (
            self.api_root
            + f"/deposit/depositions/{deposition['id']}/actions/newversion"
        )

        # Create the new version
        params = {"access_token": self.key}
        response = requests.post(url, params=params)

        if response.status_code != 201:
            msg = f"Could not create new version: {response.text}"
            self.logger.error(msg)
            raise RuntimeError(msg)

        jsr = response.json()

        # When the API creates a new version, it does not return the new one.
        # It returns the old one with a link to the new one.
        source_metadata = jsr["metadata"]
        metadata = {}

        for key, val in source_metadata.items():
            if key not in ["doi", "prereserve_doi", "publication_date"]:
                metadata[key] = val

        if version_info is None:
            previous = semantic_version.Version(jsr["metadata"]["version"])
            version_info = previous.next_major()

        metadata["version"] = str(version_info)

        new_version = self.get_deposition(f'conceptdoi:"{conceptdoi}"')
        return self.update_deposition(new_version["links"]["self"], metadata)

    def file_api_upload(self, deposition, file_name, file_handle):
        """
        Upload a file for the given deposition, using the older file API.

        Args:
            deposition: the dict of the deposition resource
            file_name: the desired file name
            file_handle: an open file handle or bytes like object.
                Must be < 100MB

        Returns:
            dict: the deposition file resource, per
            https://developers.zenodo.org/#deposition-files

        """
        url = deposition["links"]["files"]
        data = {"name": file_name, "access_token": self.key}
        files = {"file": file_handle}
        response = requests.post(url, data=data, files=files)
        jsr = response.json()

        if response.status_code != 201:
            msg = f"Failed to upload file: {jsr}"
            self.logger.error(msg)
            raise RuntimeError(msg)

        return jsr

    def bucket_api_upload(self, deposition, file_name, file_handle):
        """
        Upload a file for the given deposition, using the newer bucket API.

        Args:
            deposition: the dict of the deposition resource
            file_name: the desired file name
            file_handle: an open file handle or bytes like object.
                Must be < 100MB

        Returns:
            dict: the deposition file resource, per
            https://developers.zenodo.org/#deposition-files

        """
        url = deposition["links"]["bucket"] + "/" + file_name
        params = {"access_token": self.key}
        response = requests.put(url, params=params, data=file_handle)
        jsr = response.json()

        if response.status_code not in [200, 201]:
            msg = (
                "Failed to upload file: "
                f"code {response.status_code} / {jsr} on {deposition}"
            )
            self.logger.error(msg)
            raise RuntimeError(msg)

        return jsr

    def upload(self, deposition, file_name, file_handle):
        """
        Upload a file for the given deposition.

        Attempt using the bucket api and fall back on the file api.

        Args:
            deposition: dict of the deposition resource
            file_name: the desired file name
            file_handle: an open file handle or bytes like object.
                Must be < 100MB

        Returns:
            dict of the deposition file resource, per
                https://developers.zenodo.org/#deposition-files
        """
        try:
            jsr = self.bucket_api_upload(deposition, file_name, file_handle)
        except Exception:
            file_handle.seek(0, 0)
            jsr = self.file_api_upload(deposition, file_name, file_handle)

        return jsr

    def publish(self, deposition):
        """
        Publish a given deposition.

        Args:
            deposition: dict of the deposition

        Returns:
            dict of the published deposition, per
            https://developers.zenodo.org/#depositions
        """
        if deposition["submitted"]:
            return deposition

        response = requests.post(
            deposition["links"]["publish"], params={"access_token": self.key}
        )
        jsr = response.json()

        if response.status_code != 202:
            msg = f"Failed to publish {deposition['title']}: {json.dumps(jsr)}"
            self.logger.error(msg)
            raise RuntimeError(msg)

        return jsr
