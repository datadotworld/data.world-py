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


class FileSourceCreateRequest(object):
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
        'expand_archive': 'bool'
    }

    attribute_map = {
        'url': 'url',
        'method': 'method',
        'request_headers': 'requestHeaders',
        'request_entity': 'requestEntity',
        'oauth_token': 'oauthToken',
        'credentials': 'credentials',
        'authorization': 'authorization',
        'expand_archive': 'expandArchive'
    }

    def __init__(self, url=None, method='GET', request_headers=None, request_entity=None, oauth_token=None, credentials=None, authorization=None, expand_archive=False):
        """
        FileSourceCreateRequest - a model defined in Swagger
        """

        self._url = None
        self._method = None
        self._request_headers = None
        self._request_entity = None
        self._oauth_token = None
        self._credentials = None
        self._authorization = None
        self._expand_archive = None

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
        if expand_archive is not None:
          self.expand_archive = expand_archive

    @property
    def url(self):
        """
        Gets the url of this FileSourceCreateRequest.
        Source URL of file. Must be an http, https.

        :return: The url of this FileSourceCreateRequest.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """
        Sets the url of this FileSourceCreateRequest.
        Source URL of file. Must be an http, https.

        :param url: The url of this FileSourceCreateRequest.
        :type: str
        """
        if url is None:
            raise ValueError("Invalid value for `url`, must not be `None`")
        if url is not None and len(url) > 4096:
            raise ValueError("Invalid value for `url`, length must be less than or equal to `4096`")
        if url is not None and len(url) < 1:
            raise ValueError("Invalid value for `url`, length must be greater than or equal to `1`")
        if url is not None and not re.search('^https?:.*', url):
            raise ValueError("Invalid value for `url`, must be a follow pattern or equal to `/^https?:.*/`")

        self._url = url

    @property
    def method(self):
        """
        Gets the method of this FileSourceCreateRequest.

        :return: The method of this FileSourceCreateRequest.
        :rtype: str
        """
        return self._method

    @method.setter
    def method(self, method):
        """
        Sets the method of this FileSourceCreateRequest.

        :param method: The method of this FileSourceCreateRequest.
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
        Gets the request_headers of this FileSourceCreateRequest.
        A map of custom HTTP header name/value pairs to pass with the request.  If a `requestEntity` string is specified, this must contain a `Content-Type` header.  An `Authorization` header value will be converted to a `WebAuthorization` object and the credentials will be encrypted.  The total size of the url and custom headers must not exceed 4096 bytes in the HTTP request, including whitespace, colons and CRLF characters.

        :return: The request_headers of this FileSourceCreateRequest.
        :rtype: dict(str, str)
        """
        return self._request_headers

    @request_headers.setter
    def request_headers(self, request_headers):
        """
        Sets the request_headers of this FileSourceCreateRequest.
        A map of custom HTTP header name/value pairs to pass with the request.  If a `requestEntity` string is specified, this must contain a `Content-Type` header.  An `Authorization` header value will be converted to a `WebAuthorization` object and the credentials will be encrypted.  The total size of the url and custom headers must not exceed 4096 bytes in the HTTP request, including whitespace, colons and CRLF characters.

        :param request_headers: The request_headers of this FileSourceCreateRequest.
        :type: dict(str, str)
        """

        self._request_headers = request_headers

    @property
    def request_entity(self):
        """
        Gets the request_entity of this FileSourceCreateRequest.

        :return: The request_entity of this FileSourceCreateRequest.
        :rtype: str
        """
        return self._request_entity

    @request_entity.setter
    def request_entity(self, request_entity):
        """
        Sets the request_entity of this FileSourceCreateRequest.

        :param request_entity: The request_entity of this FileSourceCreateRequest.
        :type: str
        """
        if request_entity is not None and len(request_entity) > 10000:
            raise ValueError("Invalid value for `request_entity`, length must be less than or equal to `10000`")

        self._request_entity = request_entity

    @property
    def oauth_token(self):
        """
        Gets the oauth_token of this FileSourceCreateRequest.

        :return: The oauth_token of this FileSourceCreateRequest.
        :rtype: OauthTokenReference
        """
        return self._oauth_token

    @oauth_token.setter
    def oauth_token(self, oauth_token):
        """
        Sets the oauth_token of this FileSourceCreateRequest.

        :param oauth_token: The oauth_token of this FileSourceCreateRequest.
        :type: OauthTokenReference
        """

        self._oauth_token = oauth_token

    @property
    def credentials(self):
        """
        Gets the credentials of this FileSourceCreateRequest.

        :return: The credentials of this FileSourceCreateRequest.
        :rtype: WebCredentials
        """
        return self._credentials

    @credentials.setter
    def credentials(self, credentials):
        """
        Sets the credentials of this FileSourceCreateRequest.

        :param credentials: The credentials of this FileSourceCreateRequest.
        :type: WebCredentials
        """

        self._credentials = credentials

    @property
    def authorization(self):
        """
        Gets the authorization of this FileSourceCreateRequest.

        :return: The authorization of this FileSourceCreateRequest.
        :rtype: WebAuthorization
        """
        return self._authorization

    @authorization.setter
    def authorization(self, authorization):
        """
        Sets the authorization of this FileSourceCreateRequest.

        :param authorization: The authorization of this FileSourceCreateRequest.
        :type: WebAuthorization
        """

        self._authorization = authorization

    @property
    def expand_archive(self):
        """
        Gets the expand_archive of this FileSourceCreateRequest.
        Indicates whether compressed files should be expanded upon upload.

        :return: The expand_archive of this FileSourceCreateRequest.
        :rtype: bool
        """
        return self._expand_archive

    @expand_archive.setter
    def expand_archive(self, expand_archive):
        """
        Sets the expand_archive of this FileSourceCreateRequest.
        Indicates whether compressed files should be expanded upon upload.

        :param expand_archive: The expand_archive of this FileSourceCreateRequest.
        :type: bool
        """

        self._expand_archive = expand_archive

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
        if not isinstance(other, FileSourceCreateRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
