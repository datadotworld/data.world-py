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


class ProjectSummaryResponse(object):
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
        'owner': 'str',
        'id': 'str',
        'title': 'str',
        'objective': 'str',
        'summary': 'str',
        'version': 'str',
        'tags': 'list[str]',
        'license': 'str',
        'visibility': 'str',
        'asset_status': 'AssetStatus',
        'status': 'str',
        'created': 'str',
        'updated': 'str',
        'access_level': 'str',
        'files': 'list[FileSummaryResponse]',
        'properties': 'dict(str, object)',
        'linked_datasets': 'list[LinkedDatasetSummaryResponse]'
    }

    attribute_map = {
        'owner': 'owner',
        'id': 'id',
        'title': 'title',
        'objective': 'objective',
        'summary': 'summary',
        'version': 'version',
        'tags': 'tags',
        'license': 'license',
        'visibility': 'visibility',
        'asset_status': 'assetStatus',
        'status': 'status',
        'created': 'created',
        'updated': 'updated',
        'access_level': 'accessLevel',
        'files': 'files',
        'properties': 'properties',
        'linked_datasets': 'linkedDatasets'
    }

    def __init__(self, owner=None, id=None, title=None, objective=None, summary=None, version=None, tags=None, license=None, visibility=None, asset_status=None, status=None, created=None, updated=None, access_level=None, files=None, properties=None, linked_datasets=None):
        """
        ProjectSummaryResponse - a model defined in Swagger
        """

        self._owner = None
        self._id = None
        self._title = None
        self._objective = None
        self._summary = None
        self._version = None
        self._tags = None
        self._license = None
        self._visibility = None
        self._asset_status = None
        self._status = None
        self._created = None
        self._updated = None
        self._access_level = None
        self._files = None
        self._properties = None
        self._linked_datasets = None

        self.owner = owner
        self.id = id
        self.title = title
        if objective is not None:
          self.objective = objective
        if summary is not None:
          self.summary = summary
        self.version = version
        if tags is not None:
          self.tags = tags
        if license is not None:
          self.license = license
        self.visibility = visibility
        if asset_status is not None:
          self.asset_status = asset_status
        self.status = status
        self.created = created
        self.updated = updated
        self.access_level = access_level
        if files is not None:
          self.files = files
        if properties is not None:
          self.properties = properties
        if linked_datasets is not None:
          self.linked_datasets = linked_datasets

    @property
    def owner(self):
        """
        Gets the owner of this ProjectSummaryResponse.

        :return: The owner of this ProjectSummaryResponse.
        :rtype: str
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """
        Sets the owner of this ProjectSummaryResponse.

        :param owner: The owner of this ProjectSummaryResponse.
        :type: str
        """
        if owner is None:
            raise ValueError("Invalid value for `owner`, must not be `None`")

        self._owner = owner

    @property
    def id(self):
        """
        Gets the id of this ProjectSummaryResponse.

        :return: The id of this ProjectSummaryResponse.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ProjectSummaryResponse.

        :param id: The id of this ProjectSummaryResponse.
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")

        self._id = id

    @property
    def title(self):
        """
        Gets the title of this ProjectSummaryResponse.

        :return: The title of this ProjectSummaryResponse.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of this ProjectSummaryResponse.

        :param title: The title of this ProjectSummaryResponse.
        :type: str
        """
        if title is None:
            raise ValueError("Invalid value for `title`, must not be `None`")
        if title is not None and len(title) > 60:
            raise ValueError("Invalid value for `title`, length must be less than or equal to `60`")
        if title is not None and len(title) < 1:
            raise ValueError("Invalid value for `title`, length must be greater than or equal to `1`")

        self._title = title

    @property
    def objective(self):
        """
        Gets the objective of this ProjectSummaryResponse.

        :return: The objective of this ProjectSummaryResponse.
        :rtype: str
        """
        return self._objective

    @objective.setter
    def objective(self, objective):
        """
        Sets the objective of this ProjectSummaryResponse.

        :param objective: The objective of this ProjectSummaryResponse.
        :type: str
        """
        if objective is not None and len(objective) > 120:
            raise ValueError("Invalid value for `objective`, length must be less than or equal to `120`")
        if objective is not None and len(objective) < 0:
            raise ValueError("Invalid value for `objective`, length must be greater than or equal to `0`")

        self._objective = objective

    @property
    def summary(self):
        """
        Gets the summary of this ProjectSummaryResponse.

        :return: The summary of this ProjectSummaryResponse.
        :rtype: str
        """
        return self._summary

    @summary.setter
    def summary(self, summary):
        """
        Sets the summary of this ProjectSummaryResponse.

        :param summary: The summary of this ProjectSummaryResponse.
        :type: str
        """
        if summary is not None and len(summary) > 25000:
            raise ValueError("Invalid value for `summary`, length must be less than or equal to `25000`")
        if summary is not None and len(summary) < 0:
            raise ValueError("Invalid value for `summary`, length must be greater than or equal to `0`")

        self._summary = summary

    @property
    def version(self):
        """
        Gets the version of this ProjectSummaryResponse.

        :return: The version of this ProjectSummaryResponse.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this ProjectSummaryResponse.

        :param version: The version of this ProjectSummaryResponse.
        :type: str
        """
        if version is None:
            raise ValueError("Invalid value for `version`, must not be `None`")

        self._version = version

    @property
    def tags(self):
        """
        Gets the tags of this ProjectSummaryResponse.

        :return: The tags of this ProjectSummaryResponse.
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """
        Sets the tags of this ProjectSummaryResponse.

        :param tags: The tags of this ProjectSummaryResponse.
        :type: list[str]
        """

        self._tags = tags

    @property
    def license(self):
        """
        Gets the license of this ProjectSummaryResponse.

        :return: The license of this ProjectSummaryResponse.
        :rtype: str
        """
        return self._license

    @license.setter
    def license(self, license):
        """
        Sets the license of this ProjectSummaryResponse.

        :param license: The license of this ProjectSummaryResponse.
        :type: str
        """
        allowed_values = ["Public Domain", "PDDL", "CC-0", "CC-BY", "CDLA-Permissive-1.0", "CC-BY-IGO", "CC-BY 3.0", "CC-BY 3.0 AU", "CC-BY 3.0 IGO", "CC-BY-SA", "CC-BY-SA 3.0", "CDLA-Sharing-1.0", "CC BY-NC", "CC BY-ND", "CC BY-ND 3.0", "CC-BY 3.0 NZ", "CC-BY-NC 3.0", "CC-BY-SA 3.0", "CC BY-NC-ND", "CC-BY-NC-SA 3.0", "CC-BY-SA 3.0 NZ", "CC-BY-NC-SA 3.0 NZ", "CC-BY-NC 3.0 NZ", "CC-BY-NC-ND-NZ-3.0", "CC BY-NC-SA", "CC-BY-NC-SA 3.0", "Italian-ODL", "MIT License", "OGL", "OGL-Canada", "OGL-Nova Scotia", "OGL-UK", "OSODL", "ODC-BY", "ODC-ODbL", "Other"]
        if license not in allowed_values:
            raise ValueError(
                "Invalid value for `license` ({0}), must be one of {1}"
                .format(license, allowed_values)
            )

        self._license = license

    @property
    def visibility(self):
        """
        Gets the visibility of this ProjectSummaryResponse.

        :return: The visibility of this ProjectSummaryResponse.
        :rtype: str
        """
        return self._visibility

    @visibility.setter
    def visibility(self, visibility):
        """
        Sets the visibility of this ProjectSummaryResponse.

        :param visibility: The visibility of this ProjectSummaryResponse.
        :type: str
        """
        if visibility is None:
            raise ValueError("Invalid value for `visibility`, must not be `None`")
        allowed_values = ["OPEN", "PRIVATE"]
        if visibility not in allowed_values:
            raise ValueError(
                "Invalid value for `visibility` ({0}), must be one of {1}"
                .format(visibility, allowed_values)
            )

        self._visibility = visibility

    @property
    def asset_status(self):
        """
        Gets the asset_status of this ProjectSummaryResponse.

        :return: The asset_status of this ProjectSummaryResponse.
        :rtype: AssetStatus
        """
        return self._asset_status

    @asset_status.setter
    def asset_status(self, asset_status):
        """
        Sets the asset_status of this ProjectSummaryResponse.

        :param asset_status: The asset_status of this ProjectSummaryResponse.
        :type: AssetStatus
        """

        self._asset_status = asset_status

    @property
    def status(self):
        """
        Gets the status of this ProjectSummaryResponse.

        :return: The status of this ProjectSummaryResponse.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this ProjectSummaryResponse.

        :param status: The status of this ProjectSummaryResponse.
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")
        allowed_values = ["NEW", "INPROGRESS", "LOADED", "SYSTEMERROR"]
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def created(self):
        """
        Gets the created of this ProjectSummaryResponse.

        :return: The created of this ProjectSummaryResponse.
        :rtype: str
        """
        return self._created

    @created.setter
    def created(self, created):
        """
        Sets the created of this ProjectSummaryResponse.

        :param created: The created of this ProjectSummaryResponse.
        :type: str
        """
        if created is None:
            raise ValueError("Invalid value for `created`, must not be `None`")

        self._created = created

    @property
    def updated(self):
        """
        Gets the updated of this ProjectSummaryResponse.

        :return: The updated of this ProjectSummaryResponse.
        :rtype: str
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """
        Sets the updated of this ProjectSummaryResponse.

        :param updated: The updated of this ProjectSummaryResponse.
        :type: str
        """
        if updated is None:
            raise ValueError("Invalid value for `updated`, must not be `None`")

        self._updated = updated

    @property
    def access_level(self):
        """
        Gets the access_level of this ProjectSummaryResponse.

        :return: The access_level of this ProjectSummaryResponse.
        :rtype: str
        """
        return self._access_level

    @access_level.setter
    def access_level(self, access_level):
        """
        Sets the access_level of this ProjectSummaryResponse.

        :param access_level: The access_level of this ProjectSummaryResponse.
        :type: str
        """
        if access_level is None:
            raise ValueError("Invalid value for `access_level`, must not be `None`")
        allowed_values = ["NONE", "DISCOVER", "READ", "WRITE", "ADMIN"]
        if access_level not in allowed_values:
            raise ValueError(
                "Invalid value for `access_level` ({0}), must be one of {1}"
                .format(access_level, allowed_values)
            )

        self._access_level = access_level

    @property
    def files(self):
        """
        Gets the files of this ProjectSummaryResponse.

        :return: The files of this ProjectSummaryResponse.
        :rtype: list[FileSummaryResponse]
        """
        return self._files

    @files.setter
    def files(self, files):
        """
        Sets the files of this ProjectSummaryResponse.

        :param files: The files of this ProjectSummaryResponse.
        :type: list[FileSummaryResponse]
        """

        self._files = files

    @property
    def properties(self):
        """
        Gets the properties of this ProjectSummaryResponse.

        :return: The properties of this ProjectSummaryResponse.
        :rtype: dict(str, object)
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """
        Sets the properties of this ProjectSummaryResponse.

        :param properties: The properties of this ProjectSummaryResponse.
        :type: dict(str, object)
        """

        self._properties = properties

    @property
    def linked_datasets(self):
        """
        Gets the linked_datasets of this ProjectSummaryResponse.

        :return: The linked_datasets of this ProjectSummaryResponse.
        :rtype: list[LinkedDatasetSummaryResponse]
        """
        return self._linked_datasets

    @linked_datasets.setter
    def linked_datasets(self, linked_datasets):
        """
        Sets the linked_datasets of this ProjectSummaryResponse.

        :param linked_datasets: The linked_datasets of this ProjectSummaryResponse.
        :type: list[LinkedDatasetSummaryResponse]
        """

        self._linked_datasets = linked_datasets

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
        if not isinstance(other, ProjectSummaryResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
