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


class SetCustomStringPropertyContribution(object):
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
        'contribution_hydratables': 'list[ContributionHydratable]',
        'override_type': 'str',
        'entity_type': 'str',
        'target': 'str',
        '_property': 'str',
        'value': 'str'
    }

    attribute_map = {
        'contribution_hydratables': 'contributionHydratables',
        'override_type': 'overrideType',
        'entity_type': 'entityType',
        'target': 'target',
        '_property': 'property',
        'value': 'value'
    }

    def __init__(self, contribution_hydratables=None, override_type=None, entity_type=None, target=None, _property=None, value=None):
        """
        SetCustomStringPropertyContribution - a model defined in Swagger
        """

        self._contribution_hydratables = None
        self._override_type = None
        self._entity_type = None
        self._target = None
        self.__property = None
        self._value = None

        if contribution_hydratables is not None:
          self.contribution_hydratables = contribution_hydratables
        if override_type is not None:
          self.override_type = override_type
        self.entity_type = entity_type
        self.target = target
        self._property = _property
        if value is not None:
          self.value = value

    @property
    def contribution_hydratables(self):
        """
        Gets the contribution_hydratables of this SetCustomStringPropertyContribution.

        :return: The contribution_hydratables of this SetCustomStringPropertyContribution.
        :rtype: list[ContributionHydratable]
        """
        return self._contribution_hydratables

    @contribution_hydratables.setter
    def contribution_hydratables(self, contribution_hydratables):
        """
        Sets the contribution_hydratables of this SetCustomStringPropertyContribution.

        :param contribution_hydratables: The contribution_hydratables of this SetCustomStringPropertyContribution.
        :type: list[ContributionHydratable]
        """

        self._contribution_hydratables = contribution_hydratables

    @property
    def override_type(self):
        """
        Gets the override_type of this SetCustomStringPropertyContribution.

        :return: The override_type of this SetCustomStringPropertyContribution.
        :rtype: str
        """
        return self._override_type

    @override_type.setter
    def override_type(self, override_type):
        """
        Sets the override_type of this SetCustomStringPropertyContribution.

        :param override_type: The override_type of this SetCustomStringPropertyContribution.
        :type: str
        """
        allowed_values = ["SET", "ADD", "REMOVE"]
        if override_type not in allowed_values:
            raise ValueError(
                "Invalid value for `override_type` ({0}), must be one of {1}"
                .format(override_type, allowed_values)
            )

        self._override_type = override_type

    @property
    def entity_type(self):
        """
        Gets the entity_type of this SetCustomStringPropertyContribution.

        :return: The entity_type of this SetCustomStringPropertyContribution.
        :rtype: str
        """
        return self._entity_type

    @entity_type.setter
    def entity_type(self, entity_type):
        """
        Sets the entity_type of this SetCustomStringPropertyContribution.

        :param entity_type: The entity_type of this SetCustomStringPropertyContribution.
        :type: str
        """
        if entity_type is None:
            raise ValueError("Invalid value for `entity_type`, must not be `None`")

        self._entity_type = entity_type

    @property
    def target(self):
        """
        Gets the target of this SetCustomStringPropertyContribution.

        :return: The target of this SetCustomStringPropertyContribution.
        :rtype: str
        """
        return self._target

    @target.setter
    def target(self, target):
        """
        Sets the target of this SetCustomStringPropertyContribution.

        :param target: The target of this SetCustomStringPropertyContribution.
        :type: str
        """
        if target is None:
            raise ValueError("Invalid value for `target`, must not be `None`")

        self._target = target

    @property
    def _property(self):
        """
        Gets the _property of this SetCustomStringPropertyContribution.

        :return: The _property of this SetCustomStringPropertyContribution.
        :rtype: str
        """
        return self.__property

    @_property.setter
    def _property(self, _property):
        """
        Sets the _property of this SetCustomStringPropertyContribution.

        :param _property: The _property of this SetCustomStringPropertyContribution.
        :type: str
        """
        if _property is None:
            raise ValueError("Invalid value for `_property`, must not be `None`")

        self.__property = _property

    @property
    def value(self):
        """
        Gets the value of this SetCustomStringPropertyContribution.

        :return: The value of this SetCustomStringPropertyContribution.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this SetCustomStringPropertyContribution.

        :param value: The value of this SetCustomStringPropertyContribution.
        :type: str
        """

        self._value = value

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
        if not isinstance(other, SetCustomStringPropertyContribution):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
