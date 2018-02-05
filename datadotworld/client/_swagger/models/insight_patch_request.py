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


class InsightPatchRequest(object):
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
        'title': 'str',
        'description': 'str',
        'body': 'InsightBody',
        'source_link': 'str',
        'data_source_links': 'list[str]'
    }

    attribute_map = {
        'title': 'title',
        'description': 'description',
        'body': 'body',
        'source_link': 'sourceLink',
        'data_source_links': 'dataSourceLinks'
    }

    def __init__(self, title=None, description=None, body=None, source_link=None, data_source_links=None):
        """
        InsightPatchRequest - a model defined in Swagger
        """

        self._title = None
        self._description = None
        self._body = None
        self._source_link = None
        self._data_source_links = None

        if title is not None:
          self.title = title
        if description is not None:
          self.description = description
        if body is not None:
          self.body = body
        if source_link is not None:
          self.source_link = source_link
        if data_source_links is not None:
          self.data_source_links = data_source_links

    @property
    def title(self):
        """
        Gets the title of this InsightPatchRequest.
        Insight title.

        :return: The title of this InsightPatchRequest.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of this InsightPatchRequest.
        Insight title.

        :param title: The title of this InsightPatchRequest.
        :type: str
        """
        if title is not None and len(title) > 128:
            raise ValueError("Invalid value for `title`, length must be less than or equal to `128`")
        if title is not None and len(title) < 1:
            raise ValueError("Invalid value for `title`, length must be greater than or equal to `1`")

        self._title = title

    @property
    def description(self):
        """
        Gets the description of this InsightPatchRequest.
        Insight description.

        :return: The description of this InsightPatchRequest.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this InsightPatchRequest.
        Insight description.

        :param description: The description of this InsightPatchRequest.
        :type: str
        """
        if description is not None and len(description) > 150:
            raise ValueError("Invalid value for `description`, length must be less than or equal to `150`")

        self._description = description

    @property
    def body(self):
        """
        Gets the body of this InsightPatchRequest.

        :return: The body of this InsightPatchRequest.
        :rtype: InsightBody
        """
        return self._body

    @body.setter
    def body(self, body):
        """
        Sets the body of this InsightPatchRequest.

        :param body: The body of this InsightPatchRequest.
        :type: InsightBody
        """

        self._body = body

    @property
    def source_link(self):
        """
        Gets the source_link of this InsightPatchRequest.
        Permalink to source code or platform this insight was generated with. Allows others to replicate the steps originally used to produce the insight.

        :return: The source_link of this InsightPatchRequest.
        :rtype: str
        """
        return self._source_link

    @source_link.setter
    def source_link(self, source_link):
        """
        Sets the source_link of this InsightPatchRequest.
        Permalink to source code or platform this insight was generated with. Allows others to replicate the steps originally used to produce the insight.

        :param source_link: The source_link of this InsightPatchRequest.
        :type: str
        """

        self._source_link = source_link

    @property
    def data_source_links(self):
        """
        Gets the data_source_links of this InsightPatchRequest.
        One or more permalinks to the data sources used to generate this insight. Allows others to access the data originally used to produce the insight.

        :return: The data_source_links of this InsightPatchRequest.
        :rtype: list[str]
        """
        return self._data_source_links

    @data_source_links.setter
    def data_source_links(self, data_source_links):
        """
        Sets the data_source_links of this InsightPatchRequest.
        One or more permalinks to the data sources used to generate this insight. Allows others to access the data originally used to produce the insight.

        :param data_source_links: The data_source_links of this InsightPatchRequest.
        :type: list[str]
        """

        self._data_source_links = data_source_links

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
        if not isinstance(other, InsightPatchRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
