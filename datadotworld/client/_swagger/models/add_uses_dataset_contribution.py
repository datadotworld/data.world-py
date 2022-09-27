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


class AddUsesDatasetContribution(object):
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
        'analysis_iri': 'str',
        'dataset_iri': 'str'
    }

    attribute_map = {
        'contribution_hydratables': 'contributionHydratables',
        'override_type': 'overrideType',
        'analysis_iri': 'analysisIri',
        'dataset_iri': 'datasetIri'
    }

    def __init__(self, contribution_hydratables=None, override_type=None, analysis_iri=None, dataset_iri=None):
        """
        AddUsesDatasetContribution - a model defined in Swagger
        """

        self._contribution_hydratables = None
        self._override_type = None
        self._analysis_iri = None
        self._dataset_iri = None

        if contribution_hydratables is not None:
          self.contribution_hydratables = contribution_hydratables
        if override_type is not None:
          self.override_type = override_type
        self.analysis_iri = analysis_iri
        self.dataset_iri = dataset_iri

    @property
    def contribution_hydratables(self):
        """
        Gets the contribution_hydratables of this AddUsesDatasetContribution.

        :return: The contribution_hydratables of this AddUsesDatasetContribution.
        :rtype: list[ContributionHydratable]
        """
        return self._contribution_hydratables

    @contribution_hydratables.setter
    def contribution_hydratables(self, contribution_hydratables):
        """
        Sets the contribution_hydratables of this AddUsesDatasetContribution.

        :param contribution_hydratables: The contribution_hydratables of this AddUsesDatasetContribution.
        :type: list[ContributionHydratable]
        """

        self._contribution_hydratables = contribution_hydratables

    @property
    def override_type(self):
        """
        Gets the override_type of this AddUsesDatasetContribution.

        :return: The override_type of this AddUsesDatasetContribution.
        :rtype: str
        """
        return self._override_type

    @override_type.setter
    def override_type(self, override_type):
        """
        Sets the override_type of this AddUsesDatasetContribution.

        :param override_type: The override_type of this AddUsesDatasetContribution.
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
    def analysis_iri(self):
        """
        Gets the analysis_iri of this AddUsesDatasetContribution.

        :return: The analysis_iri of this AddUsesDatasetContribution.
        :rtype: str
        """
        return self._analysis_iri

    @analysis_iri.setter
    def analysis_iri(self, analysis_iri):
        """
        Sets the analysis_iri of this AddUsesDatasetContribution.

        :param analysis_iri: The analysis_iri of this AddUsesDatasetContribution.
        :type: str
        """
        if analysis_iri is None:
            raise ValueError("Invalid value for `analysis_iri`, must not be `None`")

        self._analysis_iri = analysis_iri

    @property
    def dataset_iri(self):
        """
        Gets the dataset_iri of this AddUsesDatasetContribution.

        :return: The dataset_iri of this AddUsesDatasetContribution.
        :rtype: str
        """
        return self._dataset_iri

    @dataset_iri.setter
    def dataset_iri(self, dataset_iri):
        """
        Sets the dataset_iri of this AddUsesDatasetContribution.

        :param dataset_iri: The dataset_iri of this AddUsesDatasetContribution.
        :type: str
        """
        if dataset_iri is None:
            raise ValueError("Invalid value for `dataset_iri`, must not be `None`")

        self._dataset_iri = dataset_iri

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
        if not isinstance(other, AddUsesDatasetContribution):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
