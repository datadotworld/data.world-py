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


class FileMetadataResponse(object):
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
        'name': 'str',
        'description': 'str',
        'labels': 'list[str]',
        'size_in_bytes': 'int',
        'created': 'str',
        'updated': 'str',
        'created_by': 'str',
        'updated_by': 'str'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'labels': 'labels',
        'size_in_bytes': 'sizeInBytes',
        'created': 'created',
        'updated': 'updated',
        'created_by': 'createdBy',
        'updated_by': 'updatedBy'
    }

    def __init__(self, name=None, description=None, labels=None, size_in_bytes=None, created=None, updated=None, created_by=None, updated_by=None):
        """
        FileMetadataResponse - a model defined in Swagger
        """

        self._name = None
        self._description = None
        self._labels = None
        self._size_in_bytes = None
        self._created = None
        self._updated = None
        self._created_by = None
        self._updated_by = None

        self.name = name
        if description is not None:
          self.description = description
        if labels is not None:
          self.labels = labels
        if size_in_bytes is not None:
          self.size_in_bytes = size_in_bytes
        self.created = created
        self.updated = updated
        if created_by is not None:
          self.created_by = created_by
        if updated_by is not None:
          self.updated_by = updated_by

    @property
    def name(self):
        """
        Gets the name of this FileMetadataResponse.

        :return: The name of this FileMetadataResponse.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this FileMetadataResponse.

        :param name: The name of this FileMetadataResponse.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")
        if name is not None and len(name) > 128:
            raise ValueError("Invalid value for `name`, length must be less than or equal to `128`")
        if name is not None and len(name) < 1:
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")
        if name is not None and not re.search('^[^\/]+$', name):
            raise ValueError("Invalid value for `name`, must be a follow pattern or equal to `/^[^\/]+$/`")

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this FileMetadataResponse.

        :return: The description of this FileMetadataResponse.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this FileMetadataResponse.

        :param description: The description of this FileMetadataResponse.
        :type: str
        """
        if description is not None and len(description) > 120:
            raise ValueError("Invalid value for `description`, length must be less than or equal to `120`")
        if description is not None and len(description) < 1:
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `1`")

        self._description = description

    @property
    def labels(self):
        """
        Gets the labels of this FileMetadataResponse.

        :return: The labels of this FileMetadataResponse.
        :rtype: list[str]
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """
        Sets the labels of this FileMetadataResponse.

        :param labels: The labels of this FileMetadataResponse.
        :type: list[str]
        """

        self._labels = labels

    @property
    def size_in_bytes(self):
        """
        Gets the size_in_bytes of this FileMetadataResponse.

        :return: The size_in_bytes of this FileMetadataResponse.
        :rtype: int
        """
        return self._size_in_bytes

    @size_in_bytes.setter
    def size_in_bytes(self, size_in_bytes):
        """
        Sets the size_in_bytes of this FileMetadataResponse.

        :param size_in_bytes: The size_in_bytes of this FileMetadataResponse.
        :type: int
        """

        self._size_in_bytes = size_in_bytes

    @property
    def created(self):
        """
        Gets the created of this FileMetadataResponse.

        :return: The created of this FileMetadataResponse.
        :rtype: str
        """
        return self._created

    @created.setter
    def created(self, created):
        """
        Sets the created of this FileMetadataResponse.

        :param created: The created of this FileMetadataResponse.
        :type: str
        """
        if created is None:
            raise ValueError("Invalid value for `created`, must not be `None`")

        self._created = created

    @property
    def updated(self):
        """
        Gets the updated of this FileMetadataResponse.

        :return: The updated of this FileMetadataResponse.
        :rtype: str
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """
        Sets the updated of this FileMetadataResponse.

        :param updated: The updated of this FileMetadataResponse.
        :type: str
        """
        if updated is None:
            raise ValueError("Invalid value for `updated`, must not be `None`")

        self._updated = updated

    @property
    def created_by(self):
        """
        Gets the created_by of this FileMetadataResponse.

        :return: The created_by of this FileMetadataResponse.
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """
        Sets the created_by of this FileMetadataResponse.

        :param created_by: The created_by of this FileMetadataResponse.
        :type: str
        """

        self._created_by = created_by

    @property
    def updated_by(self):
        """
        Gets the updated_by of this FileMetadataResponse.

        :return: The updated_by of this FileMetadataResponse.
        :rtype: str
        """
        return self._updated_by

    @updated_by.setter
    def updated_by(self, updated_by):
        """
        Sets the updated_by of this FileMetadataResponse.

        :param updated_by: The updated_by of this FileMetadataResponse.
        :type: str
        """

        self._updated_by = updated_by

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
        if not isinstance(other, FileMetadataResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
