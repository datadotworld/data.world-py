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


class WebAuthorization(object):
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
        'type': 'str',
        'credentials': 'str'
    }

    attribute_map = {
        'type': 'type',
        'credentials': 'credentials'
    }

    def __init__(self, type=None, credentials=None):
        """
        WebAuthorization - a model defined in Swagger
        """

        self._type = None
        self._credentials = None

        self.type = type
        if credentials is not None:
          self.credentials = credentials

    @property
    def type(self):
        """
        Gets the type of this WebAuthorization.

        :return: The type of this WebAuthorization.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this WebAuthorization.

        :param type: The type of this WebAuthorization.
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")
        if type is not None and len(type) > 50:
            raise ValueError("Invalid value for `type`, length must be less than or equal to `50`")
        if type is not None and len(type) < 0:
            raise ValueError("Invalid value for `type`, length must be greater than or equal to `0`")

        self._type = type

    @property
    def credentials(self):
        """
        Gets the credentials of this WebAuthorization.

        :return: The credentials of this WebAuthorization.
        :rtype: str
        """
        return self._credentials

    @credentials.setter
    def credentials(self, credentials):
        """
        Sets the credentials of this WebAuthorization.

        :param credentials: The credentials of this WebAuthorization.
        :type: str
        """
        if credentials is not None and len(credentials) > 1024:
            raise ValueError("Invalid value for `credentials`, length must be less than or equal to `1024`")
        if credentials is not None and len(credentials) < 1:
            raise ValueError("Invalid value for `credentials`, length must be greater than or equal to `1`")

        self._credentials = credentials

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
        if not isinstance(other, WebAuthorization):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
