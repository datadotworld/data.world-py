# coding: utf-8

"""
    data.world Public API (internal version)

    This is the internal version of the Swagger API generated from the Java                                             resource objects and is not visible to external users. It must be a superset                                             of the more user-friendly Swagger API maintained manually at                                             https://github.com/datadotworld/dwapi-spec.

    OpenAPI spec version: 0.21.0
    
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
        'database_source': 'DatabaseSourceReference',
        'dwcc_spec': 'DwccSpecDto',
        'view_request': 'ViewRequestDto',
        'database_metadata_spec': 'DatabaseMetadataSpecDto',
        'data_tables': 'dict(str, QueryExecutionDto)',
        'table_spec': 'SingleTableMetadataSpecDto',
        'expand_archive': 'bool',
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
        'database_source': 'databaseSource',
        'dwcc_spec': 'dwccSpec',
        'view_request': 'viewRequest',
        'database_metadata_spec': 'databaseMetadataSpec',
        'data_tables': 'dataTables',
        'table_spec': 'tableSpec',
        'expand_archive': 'expandArchive',
        'sync_status': 'syncStatus',
        'sync_summary': 'syncSummary',
        'last_sync_start': 'lastSyncStart',
        'last_sync_success': 'lastSyncSuccess',
        'last_sync_failure': 'lastSyncFailure'
    }

    def __init__(self, url=None, method=None, request_headers=None, request_entity=None, oauth_token=None, credentials=None, authorization=None, database_source=None, dwcc_spec=None, view_request=None, database_metadata_spec=None, data_tables=None, table_spec=None, expand_archive=False, sync_status=None, sync_summary=None, last_sync_start=None, last_sync_success=None, last_sync_failure=None):
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
        self._database_source = None
        self._dwcc_spec = None
        self._view_request = None
        self._database_metadata_spec = None
        self._data_tables = None
        self._table_spec = None
        self._expand_archive = None
        self._sync_status = None
        self._sync_summary = None
        self._last_sync_start = None
        self._last_sync_success = None
        self._last_sync_failure = None

        if url is not None:
          self.url = url
        if method is not None:
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
        if database_source is not None:
          self.database_source = database_source
        if dwcc_spec is not None:
          self.dwcc_spec = dwcc_spec
        if view_request is not None:
          self.view_request = view_request
        if database_metadata_spec is not None:
          self.database_metadata_spec = database_metadata_spec
        if data_tables is not None:
          self.data_tables = data_tables
        if table_spec is not None:
          self.table_spec = table_spec
        if expand_archive is not None:
          self.expand_archive = expand_archive
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

        :return: The url of this FileSourceSummaryResponse.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """
        Sets the url of this FileSourceSummaryResponse.

        :param url: The url of this FileSourceSummaryResponse.
        :type: str
        """

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

        :return: The request_headers of this FileSourceSummaryResponse.
        :rtype: dict(str, str)
        """
        return self._request_headers

    @request_headers.setter
    def request_headers(self, request_headers):
        """
        Sets the request_headers of this FileSourceSummaryResponse.

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
        if request_entity is not None and len(request_entity) < 0:
            raise ValueError("Invalid value for `request_entity`, length must be greater than or equal to `0`")

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
    def database_source(self):
        """
        Gets the database_source of this FileSourceSummaryResponse.

        :return: The database_source of this FileSourceSummaryResponse.
        :rtype: DatabaseSourceReference
        """
        return self._database_source

    @database_source.setter
    def database_source(self, database_source):
        """
        Sets the database_source of this FileSourceSummaryResponse.

        :param database_source: The database_source of this FileSourceSummaryResponse.
        :type: DatabaseSourceReference
        """

        self._database_source = database_source

    @property
    def dwcc_spec(self):
        """
        Gets the dwcc_spec of this FileSourceSummaryResponse.

        :return: The dwcc_spec of this FileSourceSummaryResponse.
        :rtype: DwccSpecDto
        """
        return self._dwcc_spec

    @dwcc_spec.setter
    def dwcc_spec(self, dwcc_spec):
        """
        Sets the dwcc_spec of this FileSourceSummaryResponse.

        :param dwcc_spec: The dwcc_spec of this FileSourceSummaryResponse.
        :type: DwccSpecDto
        """

        self._dwcc_spec = dwcc_spec

    @property
    def view_request(self):
        """
        Gets the view_request of this FileSourceSummaryResponse.

        :return: The view_request of this FileSourceSummaryResponse.
        :rtype: ViewRequestDto
        """
        return self._view_request

    @view_request.setter
    def view_request(self, view_request):
        """
        Sets the view_request of this FileSourceSummaryResponse.

        :param view_request: The view_request of this FileSourceSummaryResponse.
        :type: ViewRequestDto
        """

        self._view_request = view_request

    @property
    def database_metadata_spec(self):
        """
        Gets the database_metadata_spec of this FileSourceSummaryResponse.

        :return: The database_metadata_spec of this FileSourceSummaryResponse.
        :rtype: DatabaseMetadataSpecDto
        """
        return self._database_metadata_spec

    @database_metadata_spec.setter
    def database_metadata_spec(self, database_metadata_spec):
        """
        Sets the database_metadata_spec of this FileSourceSummaryResponse.

        :param database_metadata_spec: The database_metadata_spec of this FileSourceSummaryResponse.
        :type: DatabaseMetadataSpecDto
        """

        self._database_metadata_spec = database_metadata_spec

    @property
    def data_tables(self):
        """
        Gets the data_tables of this FileSourceSummaryResponse.

        :return: The data_tables of this FileSourceSummaryResponse.
        :rtype: dict(str, QueryExecutionDto)
        """
        return self._data_tables

    @data_tables.setter
    def data_tables(self, data_tables):
        """
        Sets the data_tables of this FileSourceSummaryResponse.

        :param data_tables: The data_tables of this FileSourceSummaryResponse.
        :type: dict(str, QueryExecutionDto)
        """

        self._data_tables = data_tables

    @property
    def table_spec(self):
        """
        Gets the table_spec of this FileSourceSummaryResponse.

        :return: The table_spec of this FileSourceSummaryResponse.
        :rtype: SingleTableMetadataSpecDto
        """
        return self._table_spec

    @table_spec.setter
    def table_spec(self, table_spec):
        """
        Sets the table_spec of this FileSourceSummaryResponse.

        :param table_spec: The table_spec of this FileSourceSummaryResponse.
        :type: SingleTableMetadataSpecDto
        """

        self._table_spec = table_spec

    @property
    def expand_archive(self):
        """
        Gets the expand_archive of this FileSourceSummaryResponse.

        :return: The expand_archive of this FileSourceSummaryResponse.
        :rtype: bool
        """
        return self._expand_archive

    @expand_archive.setter
    def expand_archive(self, expand_archive):
        """
        Sets the expand_archive of this FileSourceSummaryResponse.

        :param expand_archive: The expand_archive of this FileSourceSummaryResponse.
        :type: bool
        """

        self._expand_archive = expand_archive

    @property
    def sync_status(self):
        """
        Gets the sync_status of this FileSourceSummaryResponse.

        :return: The sync_status of this FileSourceSummaryResponse.
        :rtype: str
        """
        return self._sync_status

    @sync_status.setter
    def sync_status(self, sync_status):
        """
        Sets the sync_status of this FileSourceSummaryResponse.

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

        :return: The sync_summary of this FileSourceSummaryResponse.
        :rtype: str
        """
        return self._sync_summary

    @sync_summary.setter
    def sync_summary(self, sync_summary):
        """
        Sets the sync_summary of this FileSourceSummaryResponse.

        :param sync_summary: The sync_summary of this FileSourceSummaryResponse.
        :type: str
        """

        self._sync_summary = sync_summary

    @property
    def last_sync_start(self):
        """
        Gets the last_sync_start of this FileSourceSummaryResponse.

        :return: The last_sync_start of this FileSourceSummaryResponse.
        :rtype: str
        """
        return self._last_sync_start

    @last_sync_start.setter
    def last_sync_start(self, last_sync_start):
        """
        Sets the last_sync_start of this FileSourceSummaryResponse.

        :param last_sync_start: The last_sync_start of this FileSourceSummaryResponse.
        :type: str
        """

        self._last_sync_start = last_sync_start

    @property
    def last_sync_success(self):
        """
        Gets the last_sync_success of this FileSourceSummaryResponse.

        :return: The last_sync_success of this FileSourceSummaryResponse.
        :rtype: str
        """
        return self._last_sync_success

    @last_sync_success.setter
    def last_sync_success(self, last_sync_success):
        """
        Sets the last_sync_success of this FileSourceSummaryResponse.

        :param last_sync_success: The last_sync_success of this FileSourceSummaryResponse.
        :type: str
        """

        self._last_sync_success = last_sync_success

    @property
    def last_sync_failure(self):
        """
        Gets the last_sync_failure of this FileSourceSummaryResponse.

        :return: The last_sync_failure of this FileSourceSummaryResponse.
        :rtype: str
        """
        return self._last_sync_failure

    @last_sync_failure.setter
    def last_sync_failure(self, last_sync_failure):
        """
        Sets the last_sync_failure of this FileSourceSummaryResponse.

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
