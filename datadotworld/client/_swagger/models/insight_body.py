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


class InsightBody(object):
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
        'image_url': 'str',
        'embed_url': 'str',
        'markdown_body': 'str'
    }

    attribute_map = {
        'image_url': 'imageUrl',
        'embed_url': 'embedUrl',
        'markdown_body': 'markdownBody'
    }

    def __init__(self, image_url=None, embed_url=None, markdown_body=None):
        """
        InsightBody - a model defined in Swagger
        """

        self._image_url = None
        self._embed_url = None
        self._markdown_body = None

        if image_url is not None:
          self.image_url = image_url
        if embed_url is not None:
          self.embed_url = embed_url
        if markdown_body is not None:
          self.markdown_body = markdown_body

    @property
    def image_url(self):
        """
        Gets the image_url of this InsightBody.
        Image URL

        :return: The image_url of this InsightBody.
        :rtype: str
        """
        return self._image_url

    @image_url.setter
    def image_url(self, image_url):
        """
        Sets the image_url of this InsightBody.
        Image URL

        :param image_url: The image_url of this InsightBody.
        :type: str
        """

        self._image_url = image_url

    @property
    def embed_url(self):
        """
        Gets the embed_url of this InsightBody.
        oEmbed URL.

        :return: The embed_url of this InsightBody.
        :rtype: str
        """
        return self._embed_url

    @embed_url.setter
    def embed_url(self, embed_url):
        """
        Sets the embed_url of this InsightBody.
        oEmbed URL.

        :param embed_url: The embed_url of this InsightBody.
        :type: str
        """

        self._embed_url = embed_url

    @property
    def markdown_body(self):
        """
        Gets the markdown_body of this InsightBody.
        Markdown (deprecated)

        :return: The markdown_body of this InsightBody.
        :rtype: str
        """
        return self._markdown_body

    @markdown_body.setter
    def markdown_body(self, markdown_body):
        """
        Sets the markdown_body of this InsightBody.
        Markdown (deprecated)

        :param markdown_body: The markdown_body of this InsightBody.
        :type: str
        """
        if markdown_body is not None and len(markdown_body) > 25000:
            raise ValueError("Invalid value for `markdown_body`, length must be less than or equal to `25000`")

        self._markdown_body = markdown_body

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
        if not isinstance(other, InsightBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
