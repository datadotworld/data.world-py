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


class ConceptEntry(object):
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
        'alt_label': 'str',
        'iri': 'str',
        'pref_label': 'str'
    }

    attribute_map = {
        'alt_label': 'altLabel',
        'iri': 'iri',
        'pref_label': 'prefLabel'
    }

    def __init__(self, alt_label=None, iri=None, pref_label=None):
        """
        ConceptEntry - a model defined in Swagger
        """

        self._alt_label = None
        self._iri = None
        self._pref_label = None

        if alt_label is not None:
          self.alt_label = alt_label
        if iri is not None:
          self.iri = iri
        if pref_label is not None:
          self.pref_label = pref_label

    @property
    def alt_label(self):
        """
        Gets the alt_label of this ConceptEntry.

        :return: The alt_label of this ConceptEntry.
        :rtype: str
        """
        return self._alt_label

    @alt_label.setter
    def alt_label(self, alt_label):
        """
        Sets the alt_label of this ConceptEntry.

        :param alt_label: The alt_label of this ConceptEntry.
        :type: str
        """

        self._alt_label = alt_label

    @property
    def iri(self):
        """
        Gets the iri of this ConceptEntry.

        :return: The iri of this ConceptEntry.
        :rtype: str
        """
        return self._iri

    @iri.setter
    def iri(self, iri):
        """
        Sets the iri of this ConceptEntry.

        :param iri: The iri of this ConceptEntry.
        :type: str
        """

        self._iri = iri

    @property
    def pref_label(self):
        """
        Gets the pref_label of this ConceptEntry.

        :return: The pref_label of this ConceptEntry.
        :rtype: str
        """
        return self._pref_label

    @pref_label.setter
    def pref_label(self, pref_label):
        """
        Sets the pref_label of this ConceptEntry.

        :param pref_label: The pref_label of this ConceptEntry.
        :type: str
        """

        self._pref_label = pref_label

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
        if not isinstance(other, ConceptEntry):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
