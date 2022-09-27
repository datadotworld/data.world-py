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


class RelationshipCreateOrDeleteRequest(object):
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
        'relationship_type': 'str',
        'source_dataset_id': 'str',
        'source_id': 'str',
        'source_table_id': 'str',
        'source_type': 'str',
        'target_dataset_id': 'str',
        'target_id': 'str',
        'target_table_id': 'str',
        'target_type': 'str'
    }

    attribute_map = {
        'relationship_type': 'relationshipType',
        'source_dataset_id': 'sourceDatasetId',
        'source_id': 'sourceId',
        'source_table_id': 'sourceTableId',
        'source_type': 'sourceType',
        'target_dataset_id': 'targetDatasetId',
        'target_id': 'targetId',
        'target_table_id': 'targetTableId',
        'target_type': 'targetType'
    }

    def __init__(self, relationship_type=None, source_dataset_id=None, source_id=None, source_table_id=None, source_type=None, target_dataset_id=None, target_id=None, target_table_id=None, target_type=None):
        """
        RelationshipCreateOrDeleteRequest - a model defined in Swagger
        """

        self._relationship_type = None
        self._source_dataset_id = None
        self._source_id = None
        self._source_table_id = None
        self._source_type = None
        self._target_dataset_id = None
        self._target_id = None
        self._target_table_id = None
        self._target_type = None

        self.relationship_type = relationship_type
        if source_dataset_id is not None:
          self.source_dataset_id = source_dataset_id
        self.source_id = source_id
        if source_table_id is not None:
          self.source_table_id = source_table_id
        self.source_type = source_type
        if target_dataset_id is not None:
          self.target_dataset_id = target_dataset_id
        self.target_id = target_id
        if target_table_id is not None:
          self.target_table_id = target_table_id
        self.target_type = target_type

    @property
    def relationship_type(self):
        """
        Gets the relationship_type of this RelationshipCreateOrDeleteRequest.
        IRI of the relationship type

        :return: The relationship_type of this RelationshipCreateOrDeleteRequest.
        :rtype: str
        """
        return self._relationship_type

    @relationship_type.setter
    def relationship_type(self, relationship_type):
        """
        Sets the relationship_type of this RelationshipCreateOrDeleteRequest.
        IRI of the relationship type

        :param relationship_type: The relationship_type of this RelationshipCreateOrDeleteRequest.
        :type: str
        """
        if relationship_type is None:
            raise ValueError("Invalid value for `relationship_type`, must not be `None`")

        self._relationship_type = relationship_type

    @property
    def source_dataset_id(self):
        """
        Gets the source_dataset_id of this RelationshipCreateOrDeleteRequest.
        If source is a table or column, populate with dataset ID that contains table.

        :return: The source_dataset_id of this RelationshipCreateOrDeleteRequest.
        :rtype: str
        """
        return self._source_dataset_id

    @source_dataset_id.setter
    def source_dataset_id(self, source_dataset_id):
        """
        Sets the source_dataset_id of this RelationshipCreateOrDeleteRequest.
        If source is a table or column, populate with dataset ID that contains table.

        :param source_dataset_id: The source_dataset_id of this RelationshipCreateOrDeleteRequest.
        :type: str
        """

        self._source_dataset_id = source_dataset_id

    @property
    def source_id(self):
        """
        Gets the source_id of this RelationshipCreateOrDeleteRequest.

        :return: The source_id of this RelationshipCreateOrDeleteRequest.
        :rtype: str
        """
        return self._source_id

    @source_id.setter
    def source_id(self, source_id):
        """
        Sets the source_id of this RelationshipCreateOrDeleteRequest.

        :param source_id: The source_id of this RelationshipCreateOrDeleteRequest.
        :type: str
        """
        if source_id is None:
            raise ValueError("Invalid value for `source_id`, must not be `None`")

        self._source_id = source_id

    @property
    def source_table_id(self):
        """
        Gets the source_table_id of this RelationshipCreateOrDeleteRequest.
        If source is a column, populate with table ID that contains column.

        :return: The source_table_id of this RelationshipCreateOrDeleteRequest.
        :rtype: str
        """
        return self._source_table_id

    @source_table_id.setter
    def source_table_id(self, source_table_id):
        """
        Sets the source_table_id of this RelationshipCreateOrDeleteRequest.
        If source is a column, populate with table ID that contains column.

        :param source_table_id: The source_table_id of this RelationshipCreateOrDeleteRequest.
        :type: str
        """

        self._source_table_id = source_table_id

    @property
    def source_type(self):
        """
        Gets the source_type of this RelationshipCreateOrDeleteRequest.
        Type of sourceId.

        :return: The source_type of this RelationshipCreateOrDeleteRequest.
        :rtype: str
        """
        return self._source_type

    @source_type.setter
    def source_type(self, source_type):
        """
        Sets the source_type of this RelationshipCreateOrDeleteRequest.
        Type of sourceId.

        :param source_type: The source_type of this RelationshipCreateOrDeleteRequest.
        :type: str
        """
        if source_type is None:
            raise ValueError("Invalid value for `source_type`, must not be `None`")
        allowed_values = ["CATALOG", "ANALYSIS", "BUSINESS_TERM", "COLUMN", "DATA_TYPE", "DATASET", "PROJECT", "TABLE"]
        if source_type not in allowed_values:
            raise ValueError(
                "Invalid value for `source_type` ({0}), must be one of {1}"
                .format(source_type, allowed_values)
            )

        self._source_type = source_type

    @property
    def target_dataset_id(self):
        """
        Gets the target_dataset_id of this RelationshipCreateOrDeleteRequest.
        If target is a table or column, populate with dataset ID that contains table.

        :return: The target_dataset_id of this RelationshipCreateOrDeleteRequest.
        :rtype: str
        """
        return self._target_dataset_id

    @target_dataset_id.setter
    def target_dataset_id(self, target_dataset_id):
        """
        Sets the target_dataset_id of this RelationshipCreateOrDeleteRequest.
        If target is a table or column, populate with dataset ID that contains table.

        :param target_dataset_id: The target_dataset_id of this RelationshipCreateOrDeleteRequest.
        :type: str
        """

        self._target_dataset_id = target_dataset_id

    @property
    def target_id(self):
        """
        Gets the target_id of this RelationshipCreateOrDeleteRequest.

        :return: The target_id of this RelationshipCreateOrDeleteRequest.
        :rtype: str
        """
        return self._target_id

    @target_id.setter
    def target_id(self, target_id):
        """
        Sets the target_id of this RelationshipCreateOrDeleteRequest.

        :param target_id: The target_id of this RelationshipCreateOrDeleteRequest.
        :type: str
        """
        if target_id is None:
            raise ValueError("Invalid value for `target_id`, must not be `None`")

        self._target_id = target_id

    @property
    def target_table_id(self):
        """
        Gets the target_table_id of this RelationshipCreateOrDeleteRequest.
        If target is a column, populate with table ID that contains column.

        :return: The target_table_id of this RelationshipCreateOrDeleteRequest.
        :rtype: str
        """
        return self._target_table_id

    @target_table_id.setter
    def target_table_id(self, target_table_id):
        """
        Sets the target_table_id of this RelationshipCreateOrDeleteRequest.
        If target is a column, populate with table ID that contains column.

        :param target_table_id: The target_table_id of this RelationshipCreateOrDeleteRequest.
        :type: str
        """

        self._target_table_id = target_table_id

    @property
    def target_type(self):
        """
        Gets the target_type of this RelationshipCreateOrDeleteRequest.
        Type of targetId.

        :return: The target_type of this RelationshipCreateOrDeleteRequest.
        :rtype: str
        """
        return self._target_type

    @target_type.setter
    def target_type(self, target_type):
        """
        Sets the target_type of this RelationshipCreateOrDeleteRequest.
        Type of targetId.

        :param target_type: The target_type of this RelationshipCreateOrDeleteRequest.
        :type: str
        """
        if target_type is None:
            raise ValueError("Invalid value for `target_type`, must not be `None`")
        allowed_values = ["CATALOG", "ANALYSIS", "BUSINESS_TERM", "COLUMN", "DATA_TYPE", "DATASET", "PROJECT", "TABLE"]
        if target_type not in allowed_values:
            raise ValueError(
                "Invalid value for `target_type` ({0}), must be one of {1}"
                .format(target_type, allowed_values)
            )

        self._target_type = target_type

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
        if not isinstance(other, RelationshipCreateOrDeleteRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
