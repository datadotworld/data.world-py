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


class JsonNode(object):
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
        'boolean': 'bool',
        'int': 'bool',
        'big_decimal': 'bool',
        'big_integer': 'bool',
        'double': 'bool',
        'long': 'bool',
        'value_node': 'bool',
        'container_node': 'bool',
        'missing_node': 'bool',
        'object': 'bool',
        'pojo': 'bool',
        'integral_number': 'bool',
        'floating_point_number': 'bool',
        'short': 'bool',
        'textual': 'bool',
        'binary': 'bool',
        'float': 'bool',
        'node_type': 'str',
        'number': 'bool',
        'array': 'bool',
        'null': 'bool'
    }

    attribute_map = {
        'boolean': 'boolean',
        'int': 'int',
        'big_decimal': 'bigDecimal',
        'big_integer': 'bigInteger',
        'double': 'double',
        'long': 'long',
        'value_node': 'valueNode',
        'container_node': 'containerNode',
        'missing_node': 'missingNode',
        'object': 'object',
        'pojo': 'pojo',
        'integral_number': 'integralNumber',
        'floating_point_number': 'floatingPointNumber',
        'short': 'short',
        'textual': 'textual',
        'binary': 'binary',
        'float': 'float',
        'node_type': 'nodeType',
        'number': 'number',
        'array': 'array',
        'null': 'null'
    }

    def __init__(self, boolean=False, int=False, big_decimal=False, big_integer=False, double=False, long=False, value_node=False, container_node=False, missing_node=False, object=False, pojo=False, integral_number=False, floating_point_number=False, short=False, textual=False, binary=False, float=False, node_type=None, number=False, array=False, null=False):
        """
        JsonNode - a model defined in Swagger
        """

        self._boolean = None
        self._int = None
        self._big_decimal = None
        self._big_integer = None
        self._double = None
        self._long = None
        self._value_node = None
        self._container_node = None
        self._missing_node = None
        self._object = None
        self._pojo = None
        self._integral_number = None
        self._floating_point_number = None
        self._short = None
        self._textual = None
        self._binary = None
        self._float = None
        self._node_type = None
        self._number = None
        self._array = None
        self._null = None

        if boolean is not None:
          self.boolean = boolean
        if int is not None:
          self.int = int
        if big_decimal is not None:
          self.big_decimal = big_decimal
        if big_integer is not None:
          self.big_integer = big_integer
        if double is not None:
          self.double = double
        if long is not None:
          self.long = long
        if value_node is not None:
          self.value_node = value_node
        if container_node is not None:
          self.container_node = container_node
        if missing_node is not None:
          self.missing_node = missing_node
        if object is not None:
          self.object = object
        if pojo is not None:
          self.pojo = pojo
        if integral_number is not None:
          self.integral_number = integral_number
        if floating_point_number is not None:
          self.floating_point_number = floating_point_number
        if short is not None:
          self.short = short
        if textual is not None:
          self.textual = textual
        if binary is not None:
          self.binary = binary
        if float is not None:
          self.float = float
        if node_type is not None:
          self.node_type = node_type
        if number is not None:
          self.number = number
        if array is not None:
          self.array = array
        if null is not None:
          self.null = null

    @property
    def boolean(self):
        """
        Gets the boolean of this JsonNode.

        :return: The boolean of this JsonNode.
        :rtype: bool
        """
        return self._boolean

    @boolean.setter
    def boolean(self, boolean):
        """
        Sets the boolean of this JsonNode.

        :param boolean: The boolean of this JsonNode.
        :type: bool
        """

        self._boolean = boolean

    @property
    def int(self):
        """
        Gets the int of this JsonNode.

        :return: The int of this JsonNode.
        :rtype: bool
        """
        return self._int

    @int.setter
    def int(self, int):
        """
        Sets the int of this JsonNode.

        :param int: The int of this JsonNode.
        :type: bool
        """

        self._int = int

    @property
    def big_decimal(self):
        """
        Gets the big_decimal of this JsonNode.

        :return: The big_decimal of this JsonNode.
        :rtype: bool
        """
        return self._big_decimal

    @big_decimal.setter
    def big_decimal(self, big_decimal):
        """
        Sets the big_decimal of this JsonNode.

        :param big_decimal: The big_decimal of this JsonNode.
        :type: bool
        """

        self._big_decimal = big_decimal

    @property
    def big_integer(self):
        """
        Gets the big_integer of this JsonNode.

        :return: The big_integer of this JsonNode.
        :rtype: bool
        """
        return self._big_integer

    @big_integer.setter
    def big_integer(self, big_integer):
        """
        Sets the big_integer of this JsonNode.

        :param big_integer: The big_integer of this JsonNode.
        :type: bool
        """

        self._big_integer = big_integer

    @property
    def double(self):
        """
        Gets the double of this JsonNode.

        :return: The double of this JsonNode.
        :rtype: bool
        """
        return self._double

    @double.setter
    def double(self, double):
        """
        Sets the double of this JsonNode.

        :param double: The double of this JsonNode.
        :type: bool
        """

        self._double = double

    @property
    def long(self):
        """
        Gets the long of this JsonNode.

        :return: The long of this JsonNode.
        :rtype: bool
        """
        return self._long

    @long.setter
    def long(self, long):
        """
        Sets the long of this JsonNode.

        :param long: The long of this JsonNode.
        :type: bool
        """

        self._long = long

    @property
    def value_node(self):
        """
        Gets the value_node of this JsonNode.

        :return: The value_node of this JsonNode.
        :rtype: bool
        """
        return self._value_node

    @value_node.setter
    def value_node(self, value_node):
        """
        Sets the value_node of this JsonNode.

        :param value_node: The value_node of this JsonNode.
        :type: bool
        """

        self._value_node = value_node

    @property
    def container_node(self):
        """
        Gets the container_node of this JsonNode.

        :return: The container_node of this JsonNode.
        :rtype: bool
        """
        return self._container_node

    @container_node.setter
    def container_node(self, container_node):
        """
        Sets the container_node of this JsonNode.

        :param container_node: The container_node of this JsonNode.
        :type: bool
        """

        self._container_node = container_node

    @property
    def missing_node(self):
        """
        Gets the missing_node of this JsonNode.

        :return: The missing_node of this JsonNode.
        :rtype: bool
        """
        return self._missing_node

    @missing_node.setter
    def missing_node(self, missing_node):
        """
        Sets the missing_node of this JsonNode.

        :param missing_node: The missing_node of this JsonNode.
        :type: bool
        """

        self._missing_node = missing_node

    @property
    def object(self):
        """
        Gets the object of this JsonNode.

        :return: The object of this JsonNode.
        :rtype: bool
        """
        return self._object

    @object.setter
    def object(self, object):
        """
        Sets the object of this JsonNode.

        :param object: The object of this JsonNode.
        :type: bool
        """

        self._object = object

    @property
    def pojo(self):
        """
        Gets the pojo of this JsonNode.

        :return: The pojo of this JsonNode.
        :rtype: bool
        """
        return self._pojo

    @pojo.setter
    def pojo(self, pojo):
        """
        Sets the pojo of this JsonNode.

        :param pojo: The pojo of this JsonNode.
        :type: bool
        """

        self._pojo = pojo

    @property
    def integral_number(self):
        """
        Gets the integral_number of this JsonNode.

        :return: The integral_number of this JsonNode.
        :rtype: bool
        """
        return self._integral_number

    @integral_number.setter
    def integral_number(self, integral_number):
        """
        Sets the integral_number of this JsonNode.

        :param integral_number: The integral_number of this JsonNode.
        :type: bool
        """

        self._integral_number = integral_number

    @property
    def floating_point_number(self):
        """
        Gets the floating_point_number of this JsonNode.

        :return: The floating_point_number of this JsonNode.
        :rtype: bool
        """
        return self._floating_point_number

    @floating_point_number.setter
    def floating_point_number(self, floating_point_number):
        """
        Sets the floating_point_number of this JsonNode.

        :param floating_point_number: The floating_point_number of this JsonNode.
        :type: bool
        """

        self._floating_point_number = floating_point_number

    @property
    def short(self):
        """
        Gets the short of this JsonNode.

        :return: The short of this JsonNode.
        :rtype: bool
        """
        return self._short

    @short.setter
    def short(self, short):
        """
        Sets the short of this JsonNode.

        :param short: The short of this JsonNode.
        :type: bool
        """

        self._short = short

    @property
    def textual(self):
        """
        Gets the textual of this JsonNode.

        :return: The textual of this JsonNode.
        :rtype: bool
        """
        return self._textual

    @textual.setter
    def textual(self, textual):
        """
        Sets the textual of this JsonNode.

        :param textual: The textual of this JsonNode.
        :type: bool
        """

        self._textual = textual

    @property
    def binary(self):
        """
        Gets the binary of this JsonNode.

        :return: The binary of this JsonNode.
        :rtype: bool
        """
        return self._binary

    @binary.setter
    def binary(self, binary):
        """
        Sets the binary of this JsonNode.

        :param binary: The binary of this JsonNode.
        :type: bool
        """

        self._binary = binary

    @property
    def float(self):
        """
        Gets the float of this JsonNode.

        :return: The float of this JsonNode.
        :rtype: bool
        """
        return self._float

    @float.setter
    def float(self, float):
        """
        Sets the float of this JsonNode.

        :param float: The float of this JsonNode.
        :type: bool
        """

        self._float = float

    @property
    def node_type(self):
        """
        Gets the node_type of this JsonNode.

        :return: The node_type of this JsonNode.
        :rtype: str
        """
        return self._node_type

    @node_type.setter
    def node_type(self, node_type):
        """
        Sets the node_type of this JsonNode.

        :param node_type: The node_type of this JsonNode.
        :type: str
        """
        allowed_values = ["ARRAY", "BINARY", "BOOLEAN", "MISSING", "NULL", "NUMBER", "OBJECT", "POJO", "STRING"]
        if node_type not in allowed_values:
            raise ValueError(
                "Invalid value for `node_type` ({0}), must be one of {1}"
                .format(node_type, allowed_values)
            )

        self._node_type = node_type

    @property
    def number(self):
        """
        Gets the number of this JsonNode.

        :return: The number of this JsonNode.
        :rtype: bool
        """
        return self._number

    @number.setter
    def number(self, number):
        """
        Sets the number of this JsonNode.

        :param number: The number of this JsonNode.
        :type: bool
        """

        self._number = number

    @property
    def array(self):
        """
        Gets the array of this JsonNode.

        :return: The array of this JsonNode.
        :rtype: bool
        """
        return self._array

    @array.setter
    def array(self, array):
        """
        Sets the array of this JsonNode.

        :param array: The array of this JsonNode.
        :type: bool
        """

        self._array = array

    @property
    def null(self):
        """
        Gets the null of this JsonNode.

        :return: The null of this JsonNode.
        :rtype: bool
        """
        return self._null

    @null.setter
    def null(self, null):
        """
        Sets the null of this JsonNode.

        :param null: The null of this JsonNode.
        :type: bool
        """

        self._null = null

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
        if not isinstance(other, JsonNode):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other