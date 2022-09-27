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


class InsightCreateRequest(object):
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
        'data_source_links': 'list[str]',
        'thumbnail': 'str'
    }

    attribute_map = {
        'title': 'title',
        'description': 'description',
        'body': 'body',
        'source_link': 'sourceLink',
        'data_source_links': 'dataSourceLinks',
        'thumbnail': 'thumbnail'
    }

    def __init__(self, title=None, description=None, body=None, source_link=None, data_source_links=None, thumbnail=None):
        """
        InsightCreateRequest - a model defined in Swagger
        """

        self._title = None
        self._description = None
        self._body = None
        self._source_link = None
        self._data_source_links = None
        self._thumbnail = None

        self.title = title
        if description is not None:
          self.description = description
        self.body = body
        if source_link is not None:
          self.source_link = source_link
        if data_source_links is not None:
          self.data_source_links = data_source_links
        if thumbnail is not None:
          self.thumbnail = thumbnail

    @property
    def title(self):
        """
        Gets the title of this InsightCreateRequest.

        :return: The title of this InsightCreateRequest.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of this InsightCreateRequest.

        :param title: The title of this InsightCreateRequest.
        :type: str
        """
        if title is None:
            raise ValueError("Invalid value for `title`, must not be `None`")
        if title is not None and len(title) > 128:
            raise ValueError("Invalid value for `title`, length must be less than or equal to `128`")
        if title is not None and len(title) < 1:
            raise ValueError("Invalid value for `title`, length must be greater than or equal to `1`")

        self._title = title

    @property
    def description(self):
        """
        Gets the description of this InsightCreateRequest.

        :return: The description of this InsightCreateRequest.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this InsightCreateRequest.

        :param description: The description of this InsightCreateRequest.
        :type: str
        """
        if description is not None and len(description) > 25000:
            raise ValueError("Invalid value for `description`, length must be less than or equal to `25000`")
        if description is not None and len(description) < 0:
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `0`")

        self._description = description

    @property
    def body(self):
        """
        Gets the body of this InsightCreateRequest.

        :return: The body of this InsightCreateRequest.
        :rtype: InsightBody
        """
        return self._body

    @body.setter
    def body(self, body):
        """
        Sets the body of this InsightCreateRequest.

        :param body: The body of this InsightCreateRequest.
        :type: InsightBody
        """
        if body is None:
            raise ValueError("Invalid value for `body`, must not be `None`")

        self._body = body

    @property
    def source_link(self):
        """
        Gets the source_link of this InsightCreateRequest.

        :return: The source_link of this InsightCreateRequest.
        :rtype: str
        """
        return self._source_link

    @source_link.setter
    def source_link(self, source_link):
        """
        Sets the source_link of this InsightCreateRequest.

        :param source_link: The source_link of this InsightCreateRequest.
        :type: str
        """

        self._source_link = source_link

    @property
    def data_source_links(self):
        """
        Gets the data_source_links of this InsightCreateRequest.

        :return: The data_source_links of this InsightCreateRequest.
        :rtype: list[str]
        """
        return self._data_source_links

    @data_source_links.setter
    def data_source_links(self, data_source_links):
        """
        Sets the data_source_links of this InsightCreateRequest.

        :param data_source_links: The data_source_links of this InsightCreateRequest.
        :type: list[str]
        """

        self._data_source_links = data_source_links

    @property
    def thumbnail(self):
        """
        Gets the thumbnail of this InsightCreateRequest.

        :return: The thumbnail of this InsightCreateRequest.
        :rtype: str
        """
        return self._thumbnail

    @thumbnail.setter
    def thumbnail(self, thumbnail):
        """
        Sets the thumbnail of this InsightCreateRequest.

        :param thumbnail: The thumbnail of this InsightCreateRequest.
        :type: str
        """

        self._thumbnail = thumbnail

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
        if not isinstance(other, InsightCreateRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
