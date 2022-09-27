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


class CatalogGlossarySuggestRequest(object):
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
        'collections_to_add': 'list[str]',
        'collections_to_remove': 'list[str]',
        'title': 'str',
        'type_label': 'str',
        'description': 'str',
        'tags_to_add': 'list[str]',
        'tags_to_remove': 'list[str]',
        'message': 'str',
        'properties': 'dict(str, JsonNode)',
        'summary': 'str'
    }

    attribute_map = {
        'collections_to_add': 'collectionsToAdd',
        'collections_to_remove': 'collectionsToRemove',
        'title': 'title',
        'type_label': 'typeLabel',
        'description': 'description',
        'tags_to_add': 'tagsToAdd',
        'tags_to_remove': 'tagsToRemove',
        'message': 'message',
        'properties': 'properties',
        'summary': 'summary'
    }

    def __init__(self, collections_to_add=None, collections_to_remove=None, title=None, type_label=None, description=None, tags_to_add=None, tags_to_remove=None, message=None, properties=None, summary=None):
        """
        CatalogGlossarySuggestRequest - a model defined in Swagger
        """

        self._collections_to_add = None
        self._collections_to_remove = None
        self._title = None
        self._type_label = None
        self._description = None
        self._tags_to_add = None
        self._tags_to_remove = None
        self._message = None
        self._properties = None
        self._summary = None

        if collections_to_add is not None:
          self.collections_to_add = collections_to_add
        if collections_to_remove is not None:
          self.collections_to_remove = collections_to_remove
        if title is not None:
          self.title = title
        if type_label is not None:
          self.type_label = type_label
        if description is not None:
          self.description = description
        if tags_to_add is not None:
          self.tags_to_add = tags_to_add
        if tags_to_remove is not None:
          self.tags_to_remove = tags_to_remove
        if message is not None:
          self.message = message
        if properties is not None:
          self.properties = properties
        if summary is not None:
          self.summary = summary

    @property
    def collections_to_add(self):
        """
        Gets the collections_to_add of this CatalogGlossarySuggestRequest.
        Catalog Collection to which this metadata resource is added. Required for POST and PUT.Available catalog collection can be discovered via appropriate discovery endpoints.

        :return: The collections_to_add of this CatalogGlossarySuggestRequest.
        :rtype: list[str]
        """
        return self._collections_to_add

    @collections_to_add.setter
    def collections_to_add(self, collections_to_add):
        """
        Sets the collections_to_add of this CatalogGlossarySuggestRequest.
        Catalog Collection to which this metadata resource is added. Required for POST and PUT.Available catalog collection can be discovered via appropriate discovery endpoints.

        :param collections_to_add: The collections_to_add of this CatalogGlossarySuggestRequest.
        :type: list[str]
        """

        self._collections_to_add = collections_to_add

    @property
    def collections_to_remove(self):
        """
        Gets the collections_to_remove of this CatalogGlossarySuggestRequest.
        Catalog Collection to which this metadata resource is added. Required for POST and PUT.Available catalog collection can be discovered via appropriate discovery endpoints.

        :return: The collections_to_remove of this CatalogGlossarySuggestRequest.
        :rtype: list[str]
        """
        return self._collections_to_remove

    @collections_to_remove.setter
    def collections_to_remove(self, collections_to_remove):
        """
        Sets the collections_to_remove of this CatalogGlossarySuggestRequest.
        Catalog Collection to which this metadata resource is added. Required for POST and PUT.Available catalog collection can be discovered via appropriate discovery endpoints.

        :param collections_to_remove: The collections_to_remove of this CatalogGlossarySuggestRequest.
        :type: list[str]
        """

        self._collections_to_remove = collections_to_remove

    @property
    def title(self):
        """
        Gets the title of this CatalogGlossarySuggestRequest.
        Title of the metadata resource. Required for POST and PUT.

        :return: The title of this CatalogGlossarySuggestRequest.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of this CatalogGlossarySuggestRequest.
        Title of the metadata resource. Required for POST and PUT.

        :param title: The title of this CatalogGlossarySuggestRequest.
        :type: str
        """
        if title is not None and len(title) > 60:
            raise ValueError("Invalid value for `title`, length must be less than or equal to `60`")
        if title is not None and len(title) < 1:
            raise ValueError("Invalid value for `title`, length must be greater than or equal to `1`")

        self._title = title

    @property
    def type_label(self):
        """
        Gets the type_label of this CatalogGlossarySuggestRequest.
        Indicates the type of metadata resource. Some examples of valid values are Report, Tableau dashboard, Glossary, Table, Database view etc. Default values will be assumed if not provided. Defaults to Report for analysis resources, Glossary for Glossary resources, Table for Table resources and Column for Column resources. Once specified during creation, this cannot be changed via PATCH. Only a PUT can change the type 

        :return: The type_label of this CatalogGlossarySuggestRequest.
        :rtype: str
        """
        return self._type_label

    @type_label.setter
    def type_label(self, type_label):
        """
        Sets the type_label of this CatalogGlossarySuggestRequest.
        Indicates the type of metadata resource. Some examples of valid values are Report, Tableau dashboard, Glossary, Table, Database view etc. Default values will be assumed if not provided. Defaults to Report for analysis resources, Glossary for Glossary resources, Table for Table resources and Column for Column resources. Once specified during creation, this cannot be changed via PATCH. Only a PUT can change the type 

        :param type_label: The type_label of this CatalogGlossarySuggestRequest.
        :type: str
        """

        self._type_label = type_label

    @property
    def description(self):
        """
        Gets the description of this CatalogGlossarySuggestRequest.
        A short, but descriptive statement about the metadata resource.

        :return: The description of this CatalogGlossarySuggestRequest.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this CatalogGlossarySuggestRequest.
        A short, but descriptive statement about the metadata resource.

        :param description: The description of this CatalogGlossarySuggestRequest.
        :type: str
        """
        if description is not None and len(description) > 120:
            raise ValueError("Invalid value for `description`, length must be less than or equal to `120`")
        if description is not None and len(description) < 0:
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `0`")

        self._description = description

    @property
    def tags_to_add(self):
        """
        Gets the tags_to_add of this CatalogGlossarySuggestRequest.
        A collection of tags to identify the relevance of metadata resource. Tags with no spaces is defacto standard

        :return: The tags_to_add of this CatalogGlossarySuggestRequest.
        :rtype: list[str]
        """
        return self._tags_to_add

    @tags_to_add.setter
    def tags_to_add(self, tags_to_add):
        """
        Sets the tags_to_add of this CatalogGlossarySuggestRequest.
        A collection of tags to identify the relevance of metadata resource. Tags with no spaces is defacto standard

        :param tags_to_add: The tags_to_add of this CatalogGlossarySuggestRequest.
        :type: list[str]
        """

        self._tags_to_add = tags_to_add

    @property
    def tags_to_remove(self):
        """
        Gets the tags_to_remove of this CatalogGlossarySuggestRequest.
        A collection of tags to identify the relevance of metadata resource. Tags with no spaces is defacto standard

        :return: The tags_to_remove of this CatalogGlossarySuggestRequest.
        :rtype: list[str]
        """
        return self._tags_to_remove

    @tags_to_remove.setter
    def tags_to_remove(self, tags_to_remove):
        """
        Sets the tags_to_remove of this CatalogGlossarySuggestRequest.
        A collection of tags to identify the relevance of metadata resource. Tags with no spaces is defacto standard

        :param tags_to_remove: The tags_to_remove of this CatalogGlossarySuggestRequest.
        :type: list[str]
        """

        self._tags_to_remove = tags_to_remove

    @property
    def message(self):
        """
        Gets the message of this CatalogGlossarySuggestRequest.
        Message for the suggestion

        :return: The message of this CatalogGlossarySuggestRequest.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message of this CatalogGlossarySuggestRequest.
        Message for the suggestion

        :param message: The message of this CatalogGlossarySuggestRequest.
        :type: str
        """
        if message is not None and len(message) > 250:
            raise ValueError("Invalid value for `message`, length must be less than or equal to `250`")
        if message is not None and len(message) < 1:
            raise ValueError("Invalid value for `message`, length must be greater than or equal to `1`")

        self._message = message

    @property
    def properties(self):
        """
        Gets the properties of this CatalogGlossarySuggestRequest.
        Custom properties for the metadata resource mapped to API BindingsCan be simple name-value string pairs or nested values for a string name. See examples for details.

        :return: The properties of this CatalogGlossarySuggestRequest.
        :rtype: dict(str, JsonNode)
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """
        Sets the properties of this CatalogGlossarySuggestRequest.
        Custom properties for the metadata resource mapped to API BindingsCan be simple name-value string pairs or nested values for a string name. See examples for details.

        :param properties: The properties of this CatalogGlossarySuggestRequest.
        :type: dict(str, JsonNode)
        """

        self._properties = properties

    @property
    def summary(self):
        """
        Gets the summary of this CatalogGlossarySuggestRequest.

        :return: The summary of this CatalogGlossarySuggestRequest.
        :rtype: str
        """
        return self._summary

    @summary.setter
    def summary(self, summary):
        """
        Sets the summary of this CatalogGlossarySuggestRequest.

        :param summary: The summary of this CatalogGlossarySuggestRequest.
        :type: str
        """
        if summary is not None and len(summary) > 120:
            raise ValueError("Invalid value for `summary`, length must be less than or equal to `120`")
        if summary is not None and len(summary) < 0:
            raise ValueError("Invalid value for `summary`, length must be greater than or equal to `0`")

        self._summary = summary

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
        if not isinstance(other, CatalogGlossarySuggestRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
