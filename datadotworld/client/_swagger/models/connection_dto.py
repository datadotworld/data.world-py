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


class ConnectionDto(object):
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
        'name': 'str',
        'type': 'str',
        'host': 'str',
        'port': 'int',
        'database': 'str',
        'credentials': 'DatabaseCredentials',
        'ssh_tunnel': 'SshTunnel',
        'ssl_required': 'bool',
        'verify_server_certificate': 'bool',
        'trusted_server_certificates': 'str',
        'properties': 'dict(str, str)',
        'advanced_properties': 'dict(str, str)'
    }

    attribute_map = {
        'name': 'name',
        'type': 'type',
        'host': 'host',
        'port': 'port',
        'database': 'database',
        'credentials': 'credentials',
        'ssh_tunnel': 'sshTunnel',
        'ssl_required': 'sslRequired',
        'verify_server_certificate': 'verifyServerCertificate',
        'trusted_server_certificates': 'trustedServerCertificates',
        'properties': 'properties',
        'advanced_properties': 'advancedProperties'
    }

    def __init__(self, name=None, type=None, host=None, port=None, database=None, credentials=None, ssh_tunnel=None, ssl_required=False, verify_server_certificate=False, trusted_server_certificates=None, properties=None, advanced_properties=None):
        """
        ConnectionDto - a model defined in Swagger
        """

        self._name = None
        self._type = None
        self._host = None
        self._port = None
        self._database = None
        self._credentials = None
        self._ssh_tunnel = None
        self._ssl_required = None
        self._verify_server_certificate = None
        self._trusted_server_certificates = None
        self._properties = None
        self._advanced_properties = None

        if name is not None:
          self.name = name
        self.type = type
        self.host = host
        if port is not None:
          self.port = port
        if database is not None:
          self.database = database
        if credentials is not None:
          self.credentials = credentials
        if ssh_tunnel is not None:
          self.ssh_tunnel = ssh_tunnel
        if ssl_required is not None:
          self.ssl_required = ssl_required
        if verify_server_certificate is not None:
          self.verify_server_certificate = verify_server_certificate
        if trusted_server_certificates is not None:
          self.trusted_server_certificates = trusted_server_certificates
        if properties is not None:
          self.properties = properties
        if advanced_properties is not None:
          self.advanced_properties = advanced_properties

    @property
    def name(self):
        """
        Gets the name of this ConnectionDto.
        Connection name

        :return: The name of this ConnectionDto.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ConnectionDto.
        Connection name

        :param name: The name of this ConnectionDto.
        :type: str
        """
        if name is not None and len(name) > 1024:
            raise ValueError("Invalid value for `name`, length must be less than or equal to `1024`")
        if name is not None and len(name) < 0:
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `0`")
        if name is not None and not re.search('[\\w\\_\\.-]{0,}', name):
            raise ValueError("Invalid value for `name`, must be a follow pattern or equal to `/[\\w\\_\\.-]{0,}/`")

        self._name = name

    @property
    def type(self):
        """
        Gets the type of this ConnectionDto.
        Database Type

        :return: The type of this ConnectionDto.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this ConnectionDto.
        Database Type

        :param type: The type of this ConnectionDto.
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")

        self._type = type

    @property
    def host(self):
        """
        Gets the host of this ConnectionDto.
        Database Host

        :return: The host of this ConnectionDto.
        :rtype: str
        """
        return self._host

    @host.setter
    def host(self, host):
        """
        Sets the host of this ConnectionDto.
        Database Host

        :param host: The host of this ConnectionDto.
        :type: str
        """
        if host is None:
            raise ValueError("Invalid value for `host`, must not be `None`")

        self._host = host

    @property
    def port(self):
        """
        Gets the port of this ConnectionDto.
        Database Port

        :return: The port of this ConnectionDto.
        :rtype: int
        """
        return self._port

    @port.setter
    def port(self, port):
        """
        Sets the port of this ConnectionDto.
        Database Port

        :param port: The port of this ConnectionDto.
        :type: int
        """
        if port is not None and port > 65535:
            raise ValueError("Invalid value for `port`, must be a value less than or equal to `65535`")
        if port is not None and port < 1:
            raise ValueError("Invalid value for `port`, must be a value greater than or equal to `1`")

        self._port = port

    @property
    def database(self):
        """
        Gets the database of this ConnectionDto.
        Database/Schema Logical Name

        :return: The database of this ConnectionDto.
        :rtype: str
        """
        return self._database

    @database.setter
    def database(self, database):
        """
        Sets the database of this ConnectionDto.
        Database/Schema Logical Name

        :param database: The database of this ConnectionDto.
        :type: str
        """
        if database is not None and len(database) > 256:
            raise ValueError("Invalid value for `database`, length must be less than or equal to `256`")
        if database is not None and len(database) < 0:
            raise ValueError("Invalid value for `database`, length must be greater than or equal to `0`")
        if database is not None and not re.search('[\\w\\_]{0,}', database):
            raise ValueError("Invalid value for `database`, must be a follow pattern or equal to `/[\\w\\_]{0,}/`")

        self._database = database

    @property
    def credentials(self):
        """
        Gets the credentials of this ConnectionDto.
        Database Credentials

        :return: The credentials of this ConnectionDto.
        :rtype: DatabaseCredentials
        """
        return self._credentials

    @credentials.setter
    def credentials(self, credentials):
        """
        Sets the credentials of this ConnectionDto.
        Database Credentials

        :param credentials: The credentials of this ConnectionDto.
        :type: DatabaseCredentials
        """

        self._credentials = credentials

    @property
    def ssh_tunnel(self):
        """
        Gets the ssh_tunnel of this ConnectionDto.
        ssh tunnel configuration

        :return: The ssh_tunnel of this ConnectionDto.
        :rtype: SshTunnel
        """
        return self._ssh_tunnel

    @ssh_tunnel.setter
    def ssh_tunnel(self, ssh_tunnel):
        """
        Sets the ssh_tunnel of this ConnectionDto.
        ssh tunnel configuration

        :param ssh_tunnel: The ssh_tunnel of this ConnectionDto.
        :type: SshTunnel
        """

        self._ssh_tunnel = ssh_tunnel

    @property
    def ssl_required(self):
        """
        Gets the ssl_required of this ConnectionDto.
        Is ssl required

        :return: The ssl_required of this ConnectionDto.
        :rtype: bool
        """
        return self._ssl_required

    @ssl_required.setter
    def ssl_required(self, ssl_required):
        """
        Sets the ssl_required of this ConnectionDto.
        Is ssl required

        :param ssl_required: The ssl_required of this ConnectionDto.
        :type: bool
        """

        self._ssl_required = ssl_required

    @property
    def verify_server_certificate(self):
        """
        Gets the verify_server_certificate of this ConnectionDto.
        Should server certificate be verified

        :return: The verify_server_certificate of this ConnectionDto.
        :rtype: bool
        """
        return self._verify_server_certificate

    @verify_server_certificate.setter
    def verify_server_certificate(self, verify_server_certificate):
        """
        Sets the verify_server_certificate of this ConnectionDto.
        Should server certificate be verified

        :param verify_server_certificate: The verify_server_certificate of this ConnectionDto.
        :type: bool
        """

        self._verify_server_certificate = verify_server_certificate

    @property
    def trusted_server_certificates(self):
        """
        Gets the trusted_server_certificates of this ConnectionDto.
        trusted server certificates

        :return: The trusted_server_certificates of this ConnectionDto.
        :rtype: str
        """
        return self._trusted_server_certificates

    @trusted_server_certificates.setter
    def trusted_server_certificates(self, trusted_server_certificates):
        """
        Sets the trusted_server_certificates of this ConnectionDto.
        trusted server certificates

        :param trusted_server_certificates: The trusted_server_certificates of this ConnectionDto.
        :type: str
        """
        if trusted_server_certificates is not None and len(trusted_server_certificates) > 100000:
            raise ValueError("Invalid value for `trusted_server_certificates`, length must be less than or equal to `100000`")
        if trusted_server_certificates is not None and len(trusted_server_certificates) < 0:
            raise ValueError("Invalid value for `trusted_server_certificates`, length must be greater than or equal to `0`")

        self._trusted_server_certificates = trusted_server_certificates

    @property
    def properties(self):
        """
        Gets the properties of this ConnectionDto.
        Properties such as auto commit, isolation level etc.

        :return: The properties of this ConnectionDto.
        :rtype: dict(str, str)
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """
        Sets the properties of this ConnectionDto.
        Properties such as auto commit, isolation level etc.

        :param properties: The properties of this ConnectionDto.
        :type: dict(str, str)
        """

        self._properties = properties

    @property
    def advanced_properties(self):
        """
        Gets the advanced_properties of this ConnectionDto.
        Advanced properties

        :return: The advanced_properties of this ConnectionDto.
        :rtype: dict(str, str)
        """
        return self._advanced_properties

    @advanced_properties.setter
    def advanced_properties(self, advanced_properties):
        """
        Sets the advanced_properties of this ConnectionDto.
        Advanced properties

        :param advanced_properties: The advanced_properties of this ConnectionDto.
        :type: dict(str, str)
        """

        self._advanced_properties = advanced_properties

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
        if not isinstance(other, ConnectionDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other