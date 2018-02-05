# coding: utf-8

"""
    data.world API

    data.world is designed for data and the people who work with data.  From professional projects to open data, data.world helps you host and share your data, collaborate with your team, and capture context and conclusions as you work.   Using this API users are able to easily access data and manage their data projects regardless of language or tool of preference.  Check out our [documentation](https://dwapi.apidocs.io) for tips on how to get started, tutorials and to interact with the API right within your browser.

    OpenAPI spec version: 0.13.4
    Contact: help@data.world
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class FileSourceSummaryResponse(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'url': 'str',
        'method': 'str',
        'request_headers': 'dict(str, str)',
        'request_entity': 'str',
        'oauth_token': 'OauthTokenReference',
        'credentials': 'WebCredentials',
        'authorization': 'WebAuthorization',
        'sync_status': 'str',
        'sync_summary': 'str',
        'last_sync_start': 'str',
        'last_sync_success': 'str',
        'last_sync_failure': 'str'
    }

    attribute_map = {
        'url': 'url',
        'method': 'method',
        'request_headers': 'requestHeaders',
        'request_entity': 'requestEntity',
        'oauth_token': 'oauthToken',
        'credentials': 'credentials',
        'authorization': 'authorization',
        'sync_status': 'syncStatus',
        'sync_summary': 'syncSummary',
        'last_sync_start': 'lastSyncStart',
        'last_sync_success': 'lastSyncSuccess',
        'last_sync_failure': 'lastSyncFailure'
    }

    def __init__(self, url=None, method='GET', request_headers=None, request_entity=None, oauth_token=None, credentials=None, authorization=None, sync_status=None, sync_summary=None, last_sync_start=None, last_sync_success=None, last_sync_failure=None):
        """
        FileSourceSummaryResponse - a model defined in Swagger
        """

        self._url = None
        self._method = None
        self._request_headers = None
        self._request_entity = None
        self._oauth_token = None
        self._credentials = None
        self._authorization = None
        self._sync_status = None
        self._sync_summary = None
        self._last_sync_start = None
        self._last_sync_success = None
        self._last_sync_failure = None

        self.url = url
        self.method = method
        if request_headers is not None:
          self.request_headers = request_headers
        if request_entity is not None:
          self.request_entity = request_entity
        if oauth_token is not None:
          self.oauth_token = oauth_token
        if credentials is not None:
          self.credentials = credentials
        if authorization is not None:
          self.authorization = authorization
        self.sync_status = sync_status
        if sync_summary is not None:
          self.sync_summary = sync_summary
        if last_sync_start is not None:
          self.last_sync_start = last_sync_start
        if last_sync_success is not None:
          self.last_sync_success = last_sync_success
        if last_sync_failure is not None:
          self.last_sync_failure = last_sync_failure

    @property
    def url(self):
        """
        Gets the url of this FileSourceSummaryResponse.
        Source URL of file. Must be an http, https, or stream URL.

        :return: The url of this FileSourceSummaryResponse.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """
        Sets the url of this FileSourceSummaryResponse.
        Source URL of file. Must be an http, https, or stream URL.

        :param url: The url of this FileSourceSummaryResponse.
        :type: str
        """
        if url is None:
            raise ValueError("Invalid value for `url`, must not be `None`")
        if url is not None and len(url) > 4096:
            raise ValueError("Invalid value for `url`, length must be less than or equal to `4096`")
        if url is not None and len(url) < 1:
            raise ValueError("Invalid value for `url`, length must be greater than or equal to `1`")
        if url is not None and not re.search('^(https?|stream):.*', url):
            raise ValueError("Invalid value for `url`, must be a follow pattern or equal to `/^(https?|stream):.*/`")

        self._url = url

    @property
    def method(self):
        """
        Gets the method of this FileSourceSummaryResponse.

        :return: The method of this FileSourceSummaryResponse.
        :rtype: str
        """
        return self._method

    @method.setter
    def method(self, method):
        """
        Sets the method of this FileSourceSummaryResponse.

        :param method: The method of this FileSourceSummaryResponse.
        :type: str
        """
        if method is None:
            raise ValueError("Invalid value for `method`, must not be `None`")
        allowed_values = ["GET", "POST"]
        if method not in allowed_values:
            raise ValueError(
                "Invalid value for `method` ({0}), must be one of {1}"
                .format(method, allowed_values)
            )

        self._method = method

    @property
    def request_headers(self):
        """
        Gets the request_headers of this FileSourceSummaryResponse.
        A map of custom HTTP header name/value pairs to pass with the request.  If a `requestEntity` string is specified, this must contain a `Content-Type` header.

        :return: The request_headers of this FileSourceSummaryResponse.
        :rtype: dict(str, str)
        """
        return self._request_headers

    @request_headers.setter
    def request_headers(self, request_headers):
        """
        Sets the request_headers of this FileSourceSummaryResponse.
        A map of custom HTTP header name/value pairs to pass with the request.  If a `requestEntity` string is specified, this must contain a `Content-Type` header.

        :param request_headers: The request_headers of this FileSourceSummaryResponse.
        :type: dict(str, str)
        """

        self._request_headers = request_headers

    @property
    def request_entity(self):
        """
        Gets the request_entity of this FileSourceSummaryResponse.

        :return: The request_entity of this FileSourceSummaryResponse.
        :rtype: str
        """
        return self._request_entity

    @request_entity.setter
    def request_entity(self, request_entity):
        """
        Sets the request_entity of this FileSourceSummaryResponse.

        :param request_entity: The request_entity of this FileSourceSummaryResponse.
        :type: str
        """
        if request_entity is not None and len(request_entity) > 10000:
            raise ValueError("Invalid value for `request_entity`, length must be less than or equal to `10000`")

        self._request_entity = request_entity

    @property
    def oauth_token(self):
        """
        Gets the oauth_token of this FileSourceSummaryResponse.

        :return: The oauth_token of this FileSourceSummaryResponse.
        :rtype: OauthTokenReference
        """
        return self._oauth_token

    @oauth_token.setter
    def oauth_token(self, oauth_token):
        """
        Sets the oauth_token of this FileSourceSummaryResponse.

        :param oauth_token: The oauth_token of this FileSourceSummaryResponse.
        :type: OauthTokenReference
        """

        self._oauth_token = oauth_token

    @property
    def credentials(self):
        """
        Gets the credentials of this FileSourceSummaryResponse.

        :return: The credentials of this FileSourceSummaryResponse.
        :rtype: WebCredentials
        """
        return self._credentials

    @credentials.setter
    def credentials(self, credentials):
        """
        Sets the credentials of this FileSourceSummaryResponse.

        :param credentials: The credentials of this FileSourceSummaryResponse.
        :type: WebCredentials
        """

        self._credentials = credentials

    @property
    def authorization(self):
        """
        Gets the authorization of this FileSourceSummaryResponse.

        :return: The authorization of this FileSourceSummaryResponse.
        :rtype: WebAuthorization
        """
        return self._authorization

    @authorization.setter
    def authorization(self, authorization):
        """
        Sets the authorization of this FileSourceSummaryResponse.

        :param authorization: The authorization of this FileSourceSummaryResponse.
        :type: WebAuthorization
        """

        self._authorization = authorization

    @property
    def sync_status(self):
        """
        Gets the sync_status of this FileSourceSummaryResponse.
        Synchronization status of the file.  This status can be checked periodically after changes are made to the dataset to determine the status of asynchronous syncronization.  * `NEW`: Just created. Not yet synchronized. * `INPROGRESS`: Currently being synchronized. * `LOADED`: Successfully synchronized. * `SYSTEMERROR`: Error state due to synchronization failure.

        :return: The sync_status of this FileSourceSummaryResponse.
        :rtype: str
        """
        return self._sync_status

    @sync_status.setter
    def sync_status(self, sync_status):
        """
        Sets the sync_status of this FileSourceSummaryResponse.
        Synchronization status of the file.  This status can be checked periodically after changes are made to the dataset to determine the status of asynchronous syncronization.  * `NEW`: Just created. Not yet synchronized. * `INPROGRESS`: Currently being synchronized. * `LOADED`: Successfully synchronized. * `SYSTEMERROR`: Error state due to synchronization failure.

        :param sync_status: The sync_status of this FileSourceSummaryResponse.
        :type: str
        """
        if sync_status is None:
            raise ValueError("Invalid value for `sync_status`, must not be `None`")
        allowed_values = ["NEW", "INPROGRESS", "OK", "SYSTEMERROR"]
        if sync_status not in allowed_values:
            raise ValueError(
                "Invalid value for `sync_status` ({0}), must be one of {1}"
                .format(sync_status, allowed_values)
            )

        self._sync_status = sync_status

    @property
    def sync_summary(self):
        """
        Gets the sync_summary of this FileSourceSummaryResponse.
        Human-readable message detailing status of last failed sync.

        :return: The sync_summary of this FileSourceSummaryResponse.
        :rtype: str
        """
        return self._sync_summary

    @sync_summary.setter
    def sync_summary(self, sync_summary):
        """
        Sets the sync_summary of this FileSourceSummaryResponse.
        Human-readable message detailing status of last failed sync.

        :param sync_summary: The sync_summary of this FileSourceSummaryResponse.
        :type: str
        """

        self._sync_summary = sync_summary

    @property
    def last_sync_start(self):
        """
        Gets the last_sync_start of this FileSourceSummaryResponse.
        Date and time when synchronization last started.

        :return: The last_sync_start of this FileSourceSummaryResponse.
        :rtype: str
        """
        return self._last_sync_start

    @last_sync_start.setter
    def last_sync_start(self, last_sync_start):
        """
        Sets the last_sync_start of this FileSourceSummaryResponse.
        Date and time when synchronization last started.

        :param last_sync_start: The last_sync_start of this FileSourceSummaryResponse.
        :type: str
        """

        self._last_sync_start = last_sync_start

    @property
    def last_sync_success(self):
        """
        Gets the last_sync_success of this FileSourceSummaryResponse.
        Date and time when synchronization last finished successfully.

        :return: The last_sync_success of this FileSourceSummaryResponse.
        :rtype: str
        """
        return self._last_sync_success

    @last_sync_success.setter
    def last_sync_success(self, last_sync_success):
        """
        Sets the last_sync_success of this FileSourceSummaryResponse.
        Date and time when synchronization last finished successfully.

        :param last_sync_success: The last_sync_success of this FileSourceSummaryResponse.
        :type: str
        """

        self._last_sync_success = last_sync_success

    @property
    def last_sync_failure(self):
        """
        Gets the last_sync_failure of this FileSourceSummaryResponse.
        Date and time when synchronization last failed.

        :return: The last_sync_failure of this FileSourceSummaryResponse.
        :rtype: str
        """
        return self._last_sync_failure

    @last_sync_failure.setter
    def last_sync_failure(self, last_sync_failure):
        """
        Sets the last_sync_failure of this FileSourceSummaryResponse.
        Date and time when synchronization last failed.

        :param last_sync_failure: The last_sync_failure of this FileSourceSummaryResponse.
        :type: str
        """

        self._last_sync_failure = last_sync_failure

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, FileSourceSummaryResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
