# data.world-py
# Copyright 2017 data.world, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the
# License.
#
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.
#
# This product includes software developed at
# data.world, Inc.(http://data.world/).

from __future__ import absolute_import, division

import json
import requests

from .api_client import ApiClient


class RestApiClient(object):
    """REST API client

    :param profile: Name of the configuration profile to use
    :type profile: str optional
    """

    def __init__(self, config):
        self._config = config
        self._protocol = 'https'
        self._download_host = 'download.data.world'
        self.ApiClient = ApiClient(self._config.auth_token)


class RestApiError(Exception):
    """Exception wrapper for errors raised by requests or by
    the swagger client"""

    def __init__(self, *args, **kwargs):
        self.cause = kwargs.pop('cause', None)
        self.status, self.reason, self.body = None, None, None
        if self.cause is not None:
            if type(self.cause) is requests.RequestException:
                requests_response = self.cause.response
                if requests_response is not None:
                    self.status = requests_response.status_code
                    self.reason = requests_response.reason
                    self.body = requests_response.content
                    self.json = requests_response.json  # Delegates to requests

        self.status = kwargs.pop('status', self.status)
        self.reason = kwargs.pop('reason', self.reason)
        self.body = kwargs.pop('body', self.body)
        super(RestApiError, self).__init__(*args, **kwargs)

    def json(self):
        """Attempts to parse json in the body of response to failed requests
        Data.world often includes a JSON body for errors;
        however, there are no guarantees.
        :returns: The JSON body if one is included. Otherwise, None.
        :rtype: dict (json)
        """
        try:
            return json.loads(self.body)
        except (ValueError, TypeError):
            return None

    def __str__(self):
        return str(self.json() or self.cause)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
