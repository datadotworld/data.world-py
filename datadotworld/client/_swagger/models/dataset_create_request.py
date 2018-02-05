# coding: utf-8

"""
    data.world API

    data.world is designed for data and the people who work with data.  From professional projects to open data, data.world helps you host and share your data, collaborate with your team, and capture context and conclusions as you work.   Using this API users are able to easily access data and manage their data projects regardless of language or tool of preference.  Check out our [documentation](https://dwapi.apidocs.io) for tips on how to get started, tutorials and to interact with the API right within your browser.

    OpenAPI spec version: 0.13.4
    Contact: help@data.world
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class DatasetCreateRequest(object):
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
        'title': 'str',
        'description': 'str',
        'summary': 'str',
        'tags': 'list[str]',
        'license': 'str',
        'visibility': 'str',
        'files': 'list[FileCreateRequest]'
    }

    attribute_map = {
        'title': 'title',
        'description': 'description',
        'summary': 'summary',
        'tags': 'tags',
        'license': 'license',
        'visibility': 'visibility',
        'files': 'files'
    }

    def __init__(self, title=None, description=None, summary=None, tags=None, license=None, visibility=None, files=None):
        """
        DatasetCreateRequest - a model defined in Swagger
        """

        self._title = None
        self._description = None
        self._summary = None
        self._tags = None
        self._license = None
        self._visibility = None
        self._files = None

        if title is not None:
          self.title = title
        if description is not None:
          self.description = description
        if summary is not None:
          self.summary = summary
        if tags is not None:
          self.tags = tags
        if license is not None:
          self.license = license
        if visibility is not None:
          self.visibility = visibility
        if files is not None:
          self.files = files

    @property
    def title(self):
        """
        Gets the title of this DatasetCreateRequest.
        Dataset name.

        :return: The title of this DatasetCreateRequest.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of this DatasetCreateRequest.
        Dataset name.

        :param title: The title of this DatasetCreateRequest.
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
    def description(self):
        """
        Gets the description of this DatasetCreateRequest.
        Short dataset description.

        :return: The description of this DatasetCreateRequest.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this DatasetCreateRequest.
        Short dataset description.

        :param description: The description of this DatasetCreateRequest.
        :type: str
        """
        if description is not None and len(description) > 120:
            raise ValueError("Invalid value for `description`, length must be less than or equal to `120`")
        if description is not None and len(description) < 0:
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `0`")

        self._description = description

    @property
    def summary(self):
        """
        Gets the summary of this DatasetCreateRequest.
        Long-form dataset summary (Markdown supported).

        :return: The summary of this DatasetCreateRequest.
        :rtype: str
        """
        return self._summary

    @summary.setter
    def summary(self, summary):
        """
        Sets the summary of this DatasetCreateRequest.
        Long-form dataset summary (Markdown supported).

        :param summary: The summary of this DatasetCreateRequest.
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
        Gets the tags of this DatasetCreateRequest.
        Dataset tags. Letters numbers and spaces only (max 25 characters).

        :return: The tags of this DatasetCreateRequest.
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """
        Sets the tags of this DatasetCreateRequest.
        Dataset tags. Letters numbers and spaces only (max 25 characters).

        :param tags: The tags of this DatasetCreateRequest.
        :type: list[str]
        """

        self._tags = tags

    @property
    def license(self):
        """
        Gets the license of this DatasetCreateRequest.
        Dataset license. Find additional info for allowed values [here](https://data.world/license-help).

        :return: The license of this DatasetCreateRequest.
        :rtype: str
        """
        return self._license

    @license.setter
    def license(self, license):
        """
        Sets the license of this DatasetCreateRequest.
        Dataset license. Find additional info for allowed values [here](https://data.world/license-help).

        :param license: The license of this DatasetCreateRequest.
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
    def visibility(self):
        """
        Gets the visibility of this DatasetCreateRequest.
        Dataset visibility. `OPEN` if the dataset can be seen by any member of data.world. `PRIVATE` if the dataset can be seen by its owner and authorized collaborators.

        :return: The visibility of this DatasetCreateRequest.
        :rtype: str
        """
        return self._visibility

    @visibility.setter
    def visibility(self, visibility):
        """
        Sets the visibility of this DatasetCreateRequest.
        Dataset visibility. `OPEN` if the dataset can be seen by any member of data.world. `PRIVATE` if the dataset can be seen by its owner and authorized collaborators.

        :param visibility: The visibility of this DatasetCreateRequest.
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
    def files(self):
        """
        Gets the files of this DatasetCreateRequest.
        Initial set of files. At dataset creation time, file uploads are not supported. However, this property can be used to add files via URL.

        :return: The files of this DatasetCreateRequest.
        :rtype: list[FileCreateRequest]
        """
        return self._files

    @files.setter
    def files(self, files):
        """
        Sets the files of this DatasetCreateRequest.
        Initial set of files. At dataset creation time, file uploads are not supported. However, this property can be used to add files via URL.

        :param files: The files of this DatasetCreateRequest.
        :type: list[FileCreateRequest]
        """

        self._files = files

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
        if not isinstance(other, DatasetCreateRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
