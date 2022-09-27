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


class RejectRequestDto(object):
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
        'requestid': 'str',
        'owner': 'str',
        'resourceid': 'str'
    }

    attribute_map = {
        'requestid': 'requestid',
        'owner': 'owner',
        'resourceid': 'resourceid'
    }

    def __init__(self, requestid=None, owner=None, resourceid=None):
        """
        RejectRequestDto - a model defined in Swagger
        """

        self._requestid = None
        self._owner = None
        self._resourceid = None

        self.requestid = requestid
        if owner is not None:
          self.owner = owner
        if resourceid is not None:
          self.resourceid = resourceid

    @property
    def requestid(self):
        """
        Gets the requestid of this RejectRequestDto.
        ID of the request to reject.

        :return: The requestid of this RejectRequestDto.
        :rtype: str
        """
        return self._requestid

    @requestid.setter
    def requestid(self, requestid):
        """
        Sets the requestid of this RejectRequestDto.
        ID of the request to reject.

        :param requestid: The requestid of this RejectRequestDto.
        :type: str
        """
        if requestid is None:
            raise ValueError("Invalid value for `requestid`, must not be `None`")

        self._requestid = requestid

    @property
    def owner(self):
        """
        Gets the owner of this RejectRequestDto.
        User name and unique identifier of the user or organization a resource belongs to. Only required for dataset authorization requests.

        :return: The owner of this RejectRequestDto.
        :rtype: str
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """
        Sets the owner of this RejectRequestDto.
        User name and unique identifier of the user or organization a resource belongs to. Only required for dataset authorization requests.

        :param owner: The owner of this RejectRequestDto.
        :type: str
        """

        self._owner = owner

    @property
    def resourceid(self):
        """
        Gets the resourceid of this RejectRequestDto.
        Unique identifier of the resource. Only required for dataset authorization requests.

        :return: The resourceid of this RejectRequestDto.
        :rtype: str
        """
        return self._resourceid

    @resourceid.setter
    def resourceid(self, resourceid):
        """
        Sets the resourceid of this RejectRequestDto.
        Unique identifier of the resource. Only required for dataset authorization requests.

        :param resourceid: The resourceid of this RejectRequestDto.
        :type: str
        """

        self._resourceid = resourceid

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
        if not isinstance(other, RejectRequestDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
