import os
import sys
import requests
import urllib.parse as urlparse

from prettytable import PrettyTable

import urllib3
urllib3.disable_warnings()

class Client(object):

    def __init__(self, endpoint, token, verify=None):
        self._token = token
        self._endpoint = endpoint
        self._cli_obj = None
        self._verify = verify

    @property
    def _cli(self):
        if self._cli_obj is not None:
            return self._cli_obj
        sess = requests.Session()
        sess.headers = self._get_headers()
        sess.verify = self._verify
        return sess

    @classmethod
    def login(cls, endpoint, username, password, verify=None):
        loginURL = urlparse.urljoin(endpoint, "/api/v1/auth/login") 
        ret = requests.post(
                loginURL, verify=verify,
                json={"username": username, "password": password})
        ret.raise_for_status()
        token = ret.json().get("token", None)
        if token is None:
            raise ValueError("could not get access token")
        return cls(endpoint, token=token, verify=verify)

    def _get_headers(self):
        headers = {
            "Authorization": "Bearer %s" % self._token
        }
        return headers

    def get_vms(self):
        url = urlparse.urljoin(self._endpoint, "/api/v1/vms/")

        ret = self._cli.get(
                url)
        ret.raise_for_status()
        return ret.json()

    def get_vm(self, vmID):
        url = urlparse.urljoin(self._endpoint, "/api/v1/vms/%s" % vmID)

        ret = self._cli.get(
                url)
        ret.raise_for_status()
        return ret.json()

    def create_snapshot(self, vmID):
        url = urlparse.urljoin(
                self._endpoint,
                "/api/v1/vms/%s/snapshots/" % vmID)
        ret = self._cli.post(
                url)
        ret.raise_for_status()
        return ret.json()

    def get_snapshots(self, vmID):
        url = urlparse.urljoin(
                self._endpoint,
                "/api/v1/vms/%s/snapshots/" % vmID)
        ret = self._cli.get(
                url)
        ret.raise_for_status()
        return ret.json()

    def get_snapshot(self, vmID, snapshotID, compare_to=None, squash=False):
        url = urlparse.urljoin(
                self._endpoint,
                "/api/v1/vms/%s/snapshots/%s/" % (vmID, snapshotID))

        params = {
            "squashChunks": squash
        }
        if compare_to is not None:
            params["compareTo"] = compare_to
        ret = self._cli.get(
                url, params=params)
        ret.raise_for_status()
        return ret.json()

    def get_disk_size(self, vmID, snapID, diskID):
        url = urlparse.urljoin(
                self._endpoint,
                "/api/v1/vms/%s/snapshots/%s/disks/%s" % (
                    vmID, snapID, diskID))
        ret = self._cli.head(
                url)
        ret.raise_for_status()
        length = ret.headers.get("content-length", None)
        if length is None:
            raise Exception("failed to get content length")
        return int(length)

    def delete_snapshot(self, vmID, snapshotID):
        url = urlparse.urljoin(
                self._endpoint,
                "/api/v1/vms/%s/snapshots/%s/" % (vmID, snapshotID))
        ret = self._cli.delete(
                url)
        ret.raise_for_status()

    def delete_all_snapshots(self, vmID):
        url = urlparse.urljoin(
                self._endpoint,
                "/api/v1/vms/%s/snapshots/" % vmID)
        ret = self._cli.delete(
                url)
        ret.raise_for_status()

    def download_chunk(self, vmID, snapID, diskID, offset,
                       length, stream=False):
        url = urlparse.urljoin(
                self._endpoint,
                "/api/v1/vms/%s/snapshots/%s/disks/%s" % (
                    vmID, snapID, diskID))
        start = offset
        end = offset + length - 1

        headers = self._get_headers()
        headers["Range"] = "bytes=%s-%s" % (start, end)
        ret = requests.get(
            url, headers=headers,
            verify=self._verify, stream=stream)
        ret.raise_for_status()

        if stream:
            return ret
        return ret.content
