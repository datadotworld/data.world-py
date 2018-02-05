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


class CreateDatasetResponse(object):
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
        'message': 'str',
        'uri': 'str'
    }

    attribute_map = {
        'message': 'message',
        'uri': 'uri'
    }

    def __init__(self, message=None, uri=None):
        """
        CreateDatasetResponse - a model defined in Swagger
        """

        self._message = None
        self._uri = None

        if message is not None:
          self.message = message
        self.uri = uri

    @property
    def message(self):
        """
        Gets the message of this CreateDatasetResponse.

        :return: The message of this CreateDatasetResponse.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message of this CreateDatasetResponse.

        :param message: The message of this CreateDatasetResponse.
        :type: str
        """
        if message is not None and len(message) > 256:
            raise ValueError("Invalid value for `message`, length must be less than or equal to `256`")
        if message is not None and len(message) < 0:
            raise ValueError("Invalid value for `message`, length must be greater than or equal to `0`")

        self._message = message

    @property
    def uri(self):
        """
        Gets the uri of this CreateDatasetResponse.
        URI of newly created dataset.

        :return: The uri of this CreateDatasetResponse.
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """
        Sets the uri of this CreateDatasetResponse.
        URI of newly created dataset.

        :param uri: The uri of this CreateDatasetResponse.
        :type: str
        """
        if uri is None:
            raise ValueError("Invalid value for `uri`, must not be `None`")

        self._uri = uri

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
        if not isinstance(other, CreateDatasetResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
