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


class DatasetSummaryResponse(object):
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
        'access_level': 'str',
        'created': 'str',
        'description': 'str',
        'dois': 'list[Doi]',
        'files': 'list[FileSummaryResponse]',
        'id': 'str',
        'is_project': 'bool',
        'license': 'str',
        'owner': 'str',
        'status': 'str',
        'summary': 'str',
        'tags': 'list[str]',
        'title': 'str',
        'updated': 'str',
        'version': 'str',
        'version_dois': 'list[Doi]',
        'visibility': 'str',
        'properties': 'object'
    }

    attribute_map = {
        'access_level': 'accessLevel',
        'created': 'created',
        'description': 'description',
        'dois': 'dois',
        'files': 'files',
        'id': 'id',
        'is_project': 'isProject',
        'license': 'license',
        'owner': 'owner',
        'status': 'status',
        'summary': 'summary',
        'tags': 'tags',
        'title': 'title',
        'updated': 'updated',
        'version': 'version',
        'version_dois': 'versionDois',
        'visibility': 'visibility',
        'properties': 'properties'
    }

    def __init__(self, access_level=None, created=None, description=None, dois=None, files=None, id=None, is_project=None, license=None, owner=None, status=None, summary=None, tags=None, title=None, updated=None, version=None, version_dois=None, visibility=None, properties=None):
        """
        DatasetSummaryResponse - a model defined in Swagger
        """

        self._access_level = None
        self._created = None
        self._description = None
        self._dois = None
        self._files = None
        self._id = None
        self._is_project = None
        self._license = None
        self._owner = None
        self._status = None
        self._summary = None
        self._tags = None
        self._title = None
        self._updated = None
        self._version = None
        self._version_dois = None
        self._visibility = None
        self._properties = None

        self.access_level = access_level
        self.created = created
        if description is not None:
          self.description = description
        if dois is not None:
          self.dois = dois
        if files is not None:
          self.files = files
        self.id = id
        self.is_project = is_project
        if license is not None:
          self.license = license
        self.owner = owner
        self.status = status
        if summary is not None:
          self.summary = summary
        if tags is not None:
          self.tags = tags
        self.title = title
        self.updated = updated
        self.version = version
        if version_dois is not None:
          self.version_dois = version_dois
        self.visibility = visibility
        if properties is not None:
          self.properties = properties

    @property
    def access_level(self):
        """
        Gets the access_level of this DatasetSummaryResponse.
        The level of access the authenticated user is allowed with respect to dataset:   * `NONE` Not allowed any access.   * `READ` Allowed to know that the dataset exists, view and download data and metadata.  * `WRITE` Allowed to update data and metadata, in addition to what READ allows.  * `ADMIN` Allowed to delete dataset, in addition to what WRITE allows.

        :return: The access_level of this DatasetSummaryResponse.
        :rtype: str
        """
        return self._access_level

    @access_level.setter
    def access_level(self, access_level):
        """
        Sets the access_level of this DatasetSummaryResponse.
        The level of access the authenticated user is allowed with respect to dataset:   * `NONE` Not allowed any access.   * `READ` Allowed to know that the dataset exists, view and download data and metadata.  * `WRITE` Allowed to update data and metadata, in addition to what READ allows.  * `ADMIN` Allowed to delete dataset, in addition to what WRITE allows.

        :param access_level: The access_level of this DatasetSummaryResponse.
        :type: str
        """
        if access_level is None:
            raise ValueError("Invalid value for `access_level`, must not be `None`")

        self._access_level = access_level

    @property
    def created(self):
        """
        Gets the created of this DatasetSummaryResponse.
        Date and time when the dataset was created.

        :return: The created of this DatasetSummaryResponse.
        :rtype: str
        """
        return self._created

    @created.setter
    def created(self, created):
        """
        Sets the created of this DatasetSummaryResponse.
        Date and time when the dataset was created.

        :param created: The created of this DatasetSummaryResponse.
        :type: str
        """
        if created is None:
            raise ValueError("Invalid value for `created`, must not be `None`")

        self._created = created

    @property
    def description(self):
        """
        Gets the description of this DatasetSummaryResponse.
        Short dataset description.

        :return: The description of this DatasetSummaryResponse.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this DatasetSummaryResponse.
        Short dataset description.

        :param description: The description of this DatasetSummaryResponse.
        :type: str
        """

        self._description = description

    @property
    def dois(self):
        """
        Gets the dois of this DatasetSummaryResponse.

        :return: The dois of this DatasetSummaryResponse.
        :rtype: list[Doi]
        """
        return self._dois

    @dois.setter
    def dois(self, dois):
        """
        Sets the dois of this DatasetSummaryResponse.

        :param dois: The dois of this DatasetSummaryResponse.
        :type: list[Doi]
        """

        self._dois = dois

    @property
    def files(self):
        """
        Gets the files of this DatasetSummaryResponse.
        Initial set of files. At dataset creation time, file uploads are not supported. However, this property can be used to add files via URL.

        :return: The files of this DatasetSummaryResponse.
        :rtype: list[FileSummaryResponse]
        """
        return self._files

    @files.setter
    def files(self, files):
        """
        Sets the files of this DatasetSummaryResponse.
        Initial set of files. At dataset creation time, file uploads are not supported. However, this property can be used to add files via URL.

        :param files: The files of this DatasetSummaryResponse.
        :type: list[FileSummaryResponse]
        """

        self._files = files

    @property
    def id(self):
        """
        Gets the id of this DatasetSummaryResponse.
        Unique identifier of dataset.

        :return: The id of this DatasetSummaryResponse.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this DatasetSummaryResponse.
        Unique identifier of dataset.

        :param id: The id of this DatasetSummaryResponse.
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")

        self._id = id

    @property
    def is_project(self):
        """
        Gets the is_project of this DatasetSummaryResponse.
        Every data project on data.world comes with a default dataset linked to it. This flag indicates if the dataset is a project's default dataset. 

        :return: The is_project of this DatasetSummaryResponse.
        :rtype: bool
        """
        return self._is_project

    @is_project.setter
    def is_project(self, is_project):
        """
        Sets the is_project of this DatasetSummaryResponse.
        Every data project on data.world comes with a default dataset linked to it. This flag indicates if the dataset is a project's default dataset. 

        :param is_project: The is_project of this DatasetSummaryResponse.
        :type: bool
        """
        if is_project is None:
            raise ValueError("Invalid value for `is_project`, must not be `None`")

        self._is_project = is_project

    @property
    def license(self):
        """
        Gets the license of this DatasetSummaryResponse.
        Dataset license. Find additional info for allowed values [here](https://data.world/license-help).

        :return: The license of this DatasetSummaryResponse.
        :rtype: str
        """
        return self._license

    @license.setter
    def license(self, license):
        """
        Sets the license of this DatasetSummaryResponse.
        Dataset license. Find additional info for allowed values [here](https://data.world/license-help).

        :param license: The license of this DatasetSummaryResponse.
        :type: str
        """

        self._license = license

    @property
    def owner(self):
        """
        Gets the owner of this DatasetSummaryResponse.
        User name and unique identifier of the creator of the dataset.

        :return: The owner of this DatasetSummaryResponse.
        :rtype: str
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """
        Sets the owner of this DatasetSummaryResponse.
        User name and unique identifier of the creator of the dataset.

        :param owner: The owner of this DatasetSummaryResponse.
        :type: str
        """
        if owner is None:
            raise ValueError("Invalid value for `owner`, must not be `None`")

        self._owner = owner

    @property
    def status(self):
        """
        Gets the status of this DatasetSummaryResponse.
        Processing status of dataset.  This status can be checked periodically after changes are made to the dataset to determine the status of asynchronous processing.  * `NEW`: Just created. Not yet processed. * `INPROGRESS`: Currently being processed. * `LOADED`: Successfully processed. * `SYSTEMERROR`: Error state due to processing failure.

        :return: The status of this DatasetSummaryResponse.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this DatasetSummaryResponse.
        Processing status of dataset.  This status can be checked periodically after changes are made to the dataset to determine the status of asynchronous processing.  * `NEW`: Just created. Not yet processed. * `INPROGRESS`: Currently being processed. * `LOADED`: Successfully processed. * `SYSTEMERROR`: Error state due to processing failure.

        :param status: The status of this DatasetSummaryResponse.
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")

        self._status = status

    @property
    def summary(self):
        """
        Gets the summary of this DatasetSummaryResponse.
        Long-form dataset summary (Markdown supported).

        :return: The summary of this DatasetSummaryResponse.
        :rtype: str
        """
        return self._summary

    @summary.setter
    def summary(self, summary):
        """
        Sets the summary of this DatasetSummaryResponse.
        Long-form dataset summary (Markdown supported).

        :param summary: The summary of this DatasetSummaryResponse.
        :type: str
        """

        self._summary = summary

    @property
    def tags(self):
        """
        Gets the tags of this DatasetSummaryResponse.
        Dataset tags. Letters numbers and spaces only (max 25 characters).

        :return: The tags of this DatasetSummaryResponse.
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """
        Sets the tags of this DatasetSummaryResponse.
        Dataset tags. Letters numbers and spaces only (max 25 characters).

        :param tags: The tags of this DatasetSummaryResponse.
        :type: list[str]
        """

        self._tags = tags

    @property
    def title(self):
        """
        Gets the title of this DatasetSummaryResponse.
        Dataset name.

        :return: The title of this DatasetSummaryResponse.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of this DatasetSummaryResponse.
        Dataset name.

        :param title: The title of this DatasetSummaryResponse.
        :type: str
        """
        if title is None:
            raise ValueError("Invalid value for `title`, must not be `None`")

        self._title = title

    @property
    def updated(self):
        """
        Gets the updated of this DatasetSummaryResponse.
        Date and time when the dataset was last updated.

        :return: The updated of this DatasetSummaryResponse.
        :rtype: str
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """
        Sets the updated of this DatasetSummaryResponse.
        Date and time when the dataset was last updated.

        :param updated: The updated of this DatasetSummaryResponse.
        :type: str
        """
        if updated is None:
            raise ValueError("Invalid value for `updated`, must not be `None`")

        self._updated = updated

    @property
    def version(self):
        """
        Gets the version of this DatasetSummaryResponse.
        Dataset version

        :return: The version of this DatasetSummaryResponse.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this DatasetSummaryResponse.
        Dataset version

        :param version: The version of this DatasetSummaryResponse.
        :type: str
        """
        if version is None:
            raise ValueError("Invalid value for `version`, must not be `None`")

        self._version = version

    @property
    def version_dois(self):
        """
        Gets the version_dois of this DatasetSummaryResponse.

        :return: The version_dois of this DatasetSummaryResponse.
        :rtype: list[Doi]
        """
        return self._version_dois

    @version_dois.setter
    def version_dois(self, version_dois):
        """
        Sets the version_dois of this DatasetSummaryResponse.

        :param version_dois: The version_dois of this DatasetSummaryResponse.
        :type: list[Doi]
        """

        self._version_dois = version_dois

    @property
    def visibility(self):
        """
        Gets the visibility of this DatasetSummaryResponse.
        Dataset visibility. `OPEN` if the dataset can be seen by any member of data.world. `PRIVATE` if the dataset can be seen by its owner and authorized collaborators. `DISCOVERABLE` if the dataset can be seen by any member of data.world, but only files marked `sample` or `preview` are visible

        :return: The visibility of this DatasetSummaryResponse.
        :rtype: str
        """
        return self._visibility

    @visibility.setter
    def visibility(self, visibility):
        """
        Sets the visibility of this DatasetSummaryResponse.
        Dataset visibility. `OPEN` if the dataset can be seen by any member of data.world. `PRIVATE` if the dataset can be seen by its owner and authorized collaborators. `DISCOVERABLE` if the dataset can be seen by any member of data.world, but only files marked `sample` or `preview` are visible

        :param visibility: The visibility of this DatasetSummaryResponse.
        :type: str
        """
        if visibility is None:
            raise ValueError("Invalid value for `visibility`, must not be `None`")

        self._visibility = visibility

    @property
    def properties(self):
        """
        Gets the properties of this DatasetSummaryResponse.
        Custom metadata properties. See [/toolkit/custom-metadata](/toolkit/custom-metadata) for more information.

        :return: The properties of this DatasetSummaryResponse.
        :rtype: object
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """
        Sets the properties of this DatasetSummaryResponse.
        Custom metadata properties. See [/toolkit/custom-metadata](/toolkit/custom-metadata) for more information.

        :param properties: The properties of this DatasetSummaryResponse.
        :type: object
        """

        self._properties = properties

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
        if not isinstance(other, DatasetSummaryResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
