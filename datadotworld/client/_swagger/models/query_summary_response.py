# coding: utf-8

"""
    data.world API

    # data.world in a nutshell  data.world is a productive, secure platform for modern data teamwork.  We bring together your data practitioners, subject matter experts, and other stakeholders by removing costly barriers to data discovery, comprehension, integration, and sharing.   Everything your team needs to quickly understand and use data stays with it.   Social features and integrations encourage collaborators to ask and answer questions, share discoveries, and coordinate closely while still using their preferred tools.  Our focus on interoperability helps you enhance your own data with data from any source, including our vast and growing library of free public datasets.   Sophisticated permissions, auditing features, and more make it easy to manage who views your data and what they do with it.  # Conventions  ## Authentication  All data.world API calls require an API token.   OAuth2 is the preferred and most secure method for authenticating users of your data.world applications. Visit our [oauth documentation](https://apidocs.data.world/toolkit/oauth) for additional information. Alternatively, you can obtain a token for _personal use or testing_ by navigating to your profile settings, under the Advanced tab ([https://data.world/settings/advanced](https://data.world/settings/advanced)).  Authentication must be provided in API requests via the `Authorization` header. For example, for a user whose API token is `my_api_token`, the request header should be `Authorization: Bearer my_api_token` (note the `Bearer` prefix).  ## Content type   By default, `application/json` is the content type used in request and response bodies. Exceptions are noted in respective endpoint documentation.  ## HTTPS only   Our APIs can only be accessed via HTTPS.  # Interested in building data.world apps?  Check out our [developer portal](https://apidocs.data.world) for tips on how to get started, tutorials, and to interact with the API endpoints right within your browser.

    OpenAPI spec version: 0.21.0
    Contact: help@data.world
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class QuerySummaryResponse(object):
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
        'body': 'str',
        'created': 'str',
        'id': 'str',
        'language': 'str',
        'name': 'str',
        'owner': 'str',
        'updated': 'str',
        'version': 'str',
        'parameters': 'dict(str, QueryParameter)'
    }

    attribute_map = {
        'body': 'body',
        'created': 'created',
        'id': 'id',
        'language': 'language',
        'name': 'name',
        'owner': 'owner',
        'updated': 'updated',
        'version': 'version',
        'parameters': 'parameters'
    }

    def __init__(self, body=None, created=None, id=None, language=None, name=None, owner=None, updated=None, version=None, parameters=None):
        """
        QuerySummaryResponse - a model defined in Swagger
        """

        self._body = None
        self._created = None
        self._id = None
        self._language = None
        self._name = None
        self._owner = None
        self._updated = None
        self._version = None
        self._parameters = None

        if body is not None:
          self.body = body
        if created is not None:
          self.created = created
        if id is not None:
          self.id = id
        if language is not None:
          self.language = language
        if name is not None:
          self.name = name
        if owner is not None:
          self.owner = owner
        if updated is not None:
          self.updated = updated
        if version is not None:
          self.version = version
        if parameters is not None:
          self.parameters = parameters

    @property
    def body(self):
        """
        Gets the body of this QuerySummaryResponse.
        Query body.

        :return: The body of this QuerySummaryResponse.
        :rtype: str
        """
        return self._body

    @body.setter
    def body(self, body):
        """
        Sets the body of this QuerySummaryResponse.
        Query body.

        :param body: The body of this QuerySummaryResponse.
        :type: str
        """

        self._body = body

    @property
    def created(self):
        """
        Gets the created of this QuerySummaryResponse.
        Date and time when the query was created.

        :return: The created of this QuerySummaryResponse.
        :rtype: str
        """
        return self._created

    @created.setter
    def created(self, created):
        """
        Sets the created of this QuerySummaryResponse.
        Date and time when the query was created.

        :param created: The created of this QuerySummaryResponse.
        :type: str
        """

        self._created = created

    @property
    def id(self):
        """
        Gets the id of this QuerySummaryResponse.
        query unique identifier

        :return: The id of this QuerySummaryResponse.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this QuerySummaryResponse.
        query unique identifier

        :param id: The id of this QuerySummaryResponse.
        :type: str
        """

        self._id = id

    @property
    def language(self):
        """
        Gets the language of this QuerySummaryResponse.
        Type of language in which this query is written. Can be either 'SPARQL' or 'SQL'.

        :return: The language of this QuerySummaryResponse.
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, language):
        """
        Sets the language of this QuerySummaryResponse.
        Type of language in which this query is written. Can be either 'SPARQL' or 'SQL'.

        :param language: The language of this QuerySummaryResponse.
        :type: str
        """

        self._language = language

    @property
    def name(self):
        """
        Gets the name of this QuerySummaryResponse.
        Query name.

        :return: The name of this QuerySummaryResponse.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this QuerySummaryResponse.
        Query name.

        :param name: The name of this QuerySummaryResponse.
        :type: str
        """

        self._name = name

    @property
    def owner(self):
        """
        Gets the owner of this QuerySummaryResponse.
        User name and unique identifier of the creator of the dataset.

        :return: The owner of this QuerySummaryResponse.
        :rtype: str
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """
        Sets the owner of this QuerySummaryResponse.
        User name and unique identifier of the creator of the dataset.

        :param owner: The owner of this QuerySummaryResponse.
        :type: str
        """

        self._owner = owner

    @property
    def updated(self):
        """
        Gets the updated of this QuerySummaryResponse.
        Date and time when the query was updated.

        :return: The updated of this QuerySummaryResponse.
        :rtype: str
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """
        Sets the updated of this QuerySummaryResponse.
        Date and time when the query was updated.

        :param updated: The updated of this QuerySummaryResponse.
        :type: str
        """

        self._updated = updated

    @property
    def version(self):
        """
        Gets the version of this QuerySummaryResponse.
        Query version id.

        :return: The version of this QuerySummaryResponse.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this QuerySummaryResponse.
        Query version id.

        :param version: The version of this QuerySummaryResponse.
        :type: str
        """

        self._version = version

    @property
    def parameters(self):
        """
        Gets the parameters of this QuerySummaryResponse.
        Parameters declared in the query body

        :return: The parameters of this QuerySummaryResponse.
        :rtype: dict(str, QueryParameter)
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """
        Sets the parameters of this QuerySummaryResponse.
        Parameters declared in the query body

        :param parameters: The parameters of this QuerySummaryResponse.
        :type: dict(str, QueryParameter)
        """

        self._parameters = parameters

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
        if not isinstance(other, QuerySummaryResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
