# coding: utf-8

"""
    data.world API

    data.world's mission is to build the most meaningful, collaborative, and abundant data resource in the world, so that people who work with data can solve problems faster.&nbsp;&nbsp; In the context of that mission, this API ensures that our users are able to easily access data and manage their data projects regardless of system or tool preference.

    OpenAPI spec version: 0.2.2
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
        'created': 'str',
        'description': 'str',
        'files': 'list[FileSummaryResponse]',
        'id': 'str',
        'license': 'str',
        'owner': 'str',
        'status': 'str',
        'summary': 'str',
        'tags': 'list[str]',
        'title': 'str',
        'updated': 'str',
        'visibility': 'str'
    }

    attribute_map = {
        'created': 'created',
        'description': 'description',
        'files': 'files',
        'id': 'id',
        'license': 'license',
        'owner': 'owner',
        'status': 'status',
        'summary': 'summary',
        'tags': 'tags',
        'title': 'title',
        'updated': 'updated',
        'visibility': 'visibility'
    }

    def __init__(self, created=None, description=None, files=None, id=None, license=None, owner=None, status=None, summary=None, tags=None, title=None, updated=None, visibility=None):
        """
        DatasetSummaryResponse - a model defined in Swagger
        """

        self._created = None
        self._description = None
        self._files = None
        self._id = None
        self._license = None
        self._owner = None
        self._status = None
        self._summary = None
        self._tags = None
        self._title = None
        self._updated = None
        self._visibility = None

        self.created = created
        if description is not None:
          self.description = description
        if files is not None:
          self.files = files
        self.id = id
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
        self.visibility = visibility

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
        if description is not None and len(description) > 120:
            raise ValueError("Invalid value for `description`, length must be less than or equal to `120`")
        if description is not None and len(description) < 0:
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `0`")

        self._description = description

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
        allowed_values = ["Public Domain", "PDDL", "CC-0", "CC-BY", "ODC-BY", "CC-BY-SA", "ODC-ODbL", "CC BY-NC", "CC BY-NC-SA", "Other"]
        if license not in allowed_values:
            raise ValueError(
                "Invalid value for `license` ({0}), must be one of {1}"
                .format(license, allowed_values)
            )

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
        allowed_values = ["NEW", "INPROGRESS", "LOADED", "SYSTEMERROR"]
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"
                .format(status, allowed_values)
            )

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
        if summary is not None and len(summary) > 25000:
            raise ValueError("Invalid value for `summary`, length must be less than or equal to `25000`")
        if summary is not None and len(summary) < 0:
            raise ValueError("Invalid value for `summary`, length must be greater than or equal to `0`")

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
        if title is not None and len(title) > 60:
            raise ValueError("Invalid value for `title`, length must be less than or equal to `60`")
        if title is not None and len(title) < 0:
            raise ValueError("Invalid value for `title`, length must be greater than or equal to `0`")

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
    def visibility(self):
        """
        Gets the visibility of this DatasetSummaryResponse.
        Dataset visibility. `OPEN` if the dataset can be seen by any member of data.world. `PRIVATE` if the dataset can be seen by its owner and authorized collaborators.

        :return: The visibility of this DatasetSummaryResponse.
        :rtype: str
        """
        return self._visibility

    @visibility.setter
    def visibility(self, visibility):
        """
        Sets the visibility of this DatasetSummaryResponse.
        Dataset visibility. `OPEN` if the dataset can be seen by any member of data.world. `PRIVATE` if the dataset can be seen by its owner and authorized collaborators.

        :param visibility: The visibility of this DatasetSummaryResponse.
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
