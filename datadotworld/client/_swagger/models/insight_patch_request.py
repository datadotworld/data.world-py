# coding: utf-8

"""
    data.world API

    # data.world in a nutshell  data.world is a productive, secure platform for modern data teamwork.  We bring together your data practitioners, subject matter experts, and other stakeholders by removing costly barriers to data discovery, comprehension, integration, and sharing.   Everything your team needs to quickly understand and use data stays with it.   Social features and integrations encourage collaborators to ask and answer questions, share discoveries, and coordinate closely while still using their preferred tools.  Our focus on interoperability helps you enhance your own data with data from any source, including our vast and growing library of free public datasets.   Sophisticated permissions, auditing features, and more make it easy to manage who views your data and what they do with it.  # Conventions  ## Authentication  All data.world API calls require an API token.   OAuth2 is the preferred and most secure method for authenticating users of your data.world applications. Visit our [oauth documentation](https://apidocs.data.world/toolkit/oauth) for additional information. Alternatively, you can obtain a token for _personal use or testing_ by navigating to your profile settings, under the Advanced tab ([https://data.world/settings/advanced](https://data.world/settings/advanced)).  Authentication must be provided in API requests via the `Authorization` header. For example, for a user whose API token is `my_api_token`, the request header should be `Authorization: Bearer my_api_token` (note the `Bearer` prefix).  ## Content type   By default, `application/json` is the content type used in request and response bodies. Exceptions are noted in respective endpoint documentation.  ## HTTPS only   Our APIs can only be accessed via HTTPS.  # Interested in building data.world apps?  Check out our [developer portal](https://apidocs.data.world) for tips on how to get started, tutorials, and to interact with the API endpoints right within your browser.

    OpenAPI spec version: 0.21.0
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
        'body': 'InsightBody',
        'data_source_links': 'list[str]',
        'description': 'str',
        'source_link': 'str',
        'thumbnail': 'str',
        'title': 'str'
    }

    attribute_map = {
        'body': 'body',
        'data_source_links': 'dataSourceLinks',
        'description': 'description',
        'source_link': 'sourceLink',
        'thumbnail': 'thumbnail',
        'title': 'title'
    }

    def __init__(self, body=None, data_source_links=None, description=None, source_link=None, thumbnail=None, title=None):
        """
        InsightPatchRequest - a model defined in Swagger
        """

        self._body = None
        self._data_source_links = None
        self._description = None
        self._source_link = None
        self._thumbnail = None
        self._title = None

        if body is not None:
          self.body = body
        if data_source_links is not None:
          self.data_source_links = data_source_links
        if description is not None:
          self.description = description
        if source_link is not None:
          self.source_link = source_link
        if thumbnail is not None:
          self.thumbnail = thumbnail
        if title is not None:
          self.title = title

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
        if description is not None and len(description) > 25000:
            raise ValueError("Invalid value for `description`, length must be less than or equal to `25000`")

        self._description = description

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
    def thumbnail(self):
        """
        Gets the thumbnail of this InsightPatchRequest.

        :return: The thumbnail of this InsightPatchRequest.
        :rtype: str
        """
        return self._thumbnail

    @thumbnail.setter
    def thumbnail(self, thumbnail):
        """
        Sets the thumbnail of this InsightPatchRequest.

        :param thumbnail: The thumbnail of this InsightPatchRequest.
        :type: str
        """

        self._thumbnail = thumbnail

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
