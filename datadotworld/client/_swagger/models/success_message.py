# coding: utf-8

"""
    data.world API

    data.world's mission is to build the most meaningful, collaborative, and abundant data resource in the world, so that people who work with data can solve problems faster.&nbsp;&nbsp; In the context of that mission, this API ensures that our users are able to easily access data and manage their data projects regardless of system or tool preference.

    OpenAPI spec version: 0.4.0
    Contact: help@data.world
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class SuccessMessage(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, message=None):
        """
        SuccessMessage - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'message': 'str'
        }

        self.attribute_map = {
            'message': 'message'
        }

        self._message = message

    @property
    def message(self):
        """
        Gets the message of this SuccessMessage.

        :return: The message of this SuccessMessage.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message of this SuccessMessage.

        :param message: The message of this SuccessMessage.
        :type: str
        """
        if message is not None and len(message) > 256:
            raise ValueError("Invalid value for `message`, length must be less than or equal to `256`")
        if message is not None and len(message) < 0:
            raise ValueError("Invalid value for `message`, length must be greater than or equal to `0`")

        self._message = message

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
        if not isinstance(other, SuccessMessage):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
