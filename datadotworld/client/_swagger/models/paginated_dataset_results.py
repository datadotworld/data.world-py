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


class PaginatedDatasetResults(object):
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
        'count': 'int',
        'records': 'list[DatasetSummaryResponse]',
        'next_page_token': 'str'
    }

    attribute_map = {
        'count': 'count',
        'records': 'records',
        'next_page_token': 'nextPageToken'
    }

    def __init__(self, count=None, records=None, next_page_token=None):
        """
        PaginatedDatasetResults - a model defined in Swagger
        """

        self._count = None
        self._records = None
        self._next_page_token = None

        self.count = count
        self.records = records
        if next_page_token is not None:
          self.next_page_token = next_page_token

    @property
    def count(self):
        """
        Gets the count of this PaginatedDatasetResults.

        :return: The count of this PaginatedDatasetResults.
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """
        Sets the count of this PaginatedDatasetResults.

        :param count: The count of this PaginatedDatasetResults.
        :type: int
        """
        if count is None:
            raise ValueError("Invalid value for `count`, must not be `None`")
        if count is not None and count < 0:
            raise ValueError("Invalid value for `count`, must be a value greater than or equal to `0`")

        self._count = count

    @property
    def records(self):
        """
        Gets the records of this PaginatedDatasetResults.

        :return: The records of this PaginatedDatasetResults.
        :rtype: list[DatasetSummaryResponse]
        """
        return self._records

    @records.setter
    def records(self, records):
        """
        Sets the records of this PaginatedDatasetResults.

        :param records: The records of this PaginatedDatasetResults.
        :type: list[DatasetSummaryResponse]
        """
        if records is None:
            raise ValueError("Invalid value for `records`, must not be `None`")

        self._records = records

    @property
    def next_page_token(self):
        """
        Gets the next_page_token of this PaginatedDatasetResults.

        :return: The next_page_token of this PaginatedDatasetResults.
        :rtype: str
        """
        return self._next_page_token

    @next_page_token.setter
    def next_page_token(self, next_page_token):
        """
        Sets the next_page_token of this PaginatedDatasetResults.

        :param next_page_token: The next_page_token of this PaginatedDatasetResults.
        :type: str
        """

        self._next_page_token = next_page_token

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
        if not isinstance(other, PaginatedDatasetResults):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
