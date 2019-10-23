"""Module for classes that format variables."""


class SNMPAuth(object):
    """Variable representation for data for SNMP polling."""

    def __init__(self, version=2, community='public', port=161,
                 secname=None,
                 authprotocol=None, authpassword=None,
                 privprotocol=None, privpassword=None):
        """Initialize the class.

        Args:
            version: SNMP version
            community: SNMP community
            port: SNMP port
            secname: SNMP secname
            authprotocol: SNMP authprotocol
            authpassword: SNMP authpassword
            privprotocol: SNMP privprotocol
            privpassword: SNMP privpassword
            ip_devices: Devices that have these SNMP security parameters

        Returns:
            None

        """
        # Initialize variables
        self.port = 161
        self.version = 2
        self.community = 'public'
        self.secname = None
        self.authprotocol = None
        self.authpassword = None
        self.privprotocol = None
        self.privpassword = None

        # Set variables
        self.port = int(port)
        self.version = int(version)
        if self.version in [1, 2]:
            self.community = community
            self.secname = None
            self.authprotocol = None
            self.authpassword = None
            self.privprotocol = None
            self.privpassword = None
        else:
            self.community = None
            self.secname = secname
            self.authpassword = authpassword
            self.privpassword = privpassword
            if isinstance(authprotocol, str) is True and (
                    authprotocol.upper() in ['MD5', 'SHA']):
                self.authprotocol = authprotocol.upper()
            if isinstance(privprotocol, str) is True and (
                    privprotocol.upper() in ['DES', 'AES']):
                self.privprotocol = privprotocol.upper()

    def __repr__(self):
        """Return a representation of the attributes of the class.

        Args:
            None

        Returns:
            result: String representation.

        """
        # Return repr
        return (
            '<{0} version={2}, community={3}, port={8}, secname={4}, '
            'authprotocol={1} authpassword={5}, '
            'privpassword={6}, privprotocol={7}>'
            ''.format(
                self.__class__.__name__,
                repr(self.authprotocol), repr(self.version),
                repr(self.community), repr(self.secname),
                repr(self.authpassword), repr(self.privpassword),
                repr(self.privprotocol), repr(self.port)
            )
        )


class SNMPVariable(object):
    """Variable representation for data for SNMP polling."""

    def __init__(self, snmpauth=None, ip_device=None):
        """Initialize the class.

        Args:
            snmpauth: SNMPAuth object
            ip_device: Devices for these SNMP security parameters

        Returns:
            None

        """
        # Initialize variables
        self.snmpauth = None
        self.ip_device = None

        # Assign variables
        if isinstance(snmpauth, SNMPAuth) is True:
            self.snmpauth = snmpauth
        if isinstance(ip_device, str) is True:
            self.ip_device = ip_device
        self.active = False not in [bool(self.snmpauth), bool(self.ip_device)]

    def __repr__(self):
        """Return a representation of the attributes of the class.

        Args:
            None

        Returns:
            result: String representation.

        """
        # Return repr
        return (
            '<{0} snmpauth={1}, ip_device={2}, active={3}>'
            ''.format(
                self.__class__.__name__,
                repr(self.snmpauth), repr(self.ip_device),
                repr(self.active)
            )
        )


class SNMPVariableList(object):
    """Variable representation for data for SNMP polling."""

    def __init__(self, snmpauth=None, ip_devices=None):
        """Initialize the class.

        Args:
            snmpauth: SNMPAuth authentication parameters
            ip_devices: Devices needing snmpauth

        Returns:
            None

        """
        # Initialize variables
        self.snmpvariables = []
        if isinstance(ip_devices, str) is True:
            _ip_devices = [ip_devices]
        elif isinstance(ip_devices, list) is True:
            _ip_devices = ip_devices
        else:
            _ip_devices = []

        # Append to the SNMP list
        for ip_device in _ip_devices:
            snmpvariable = SNMPVariable(
                snmpauth=snmpauth, ip_device=ip_device)
            if snmpvariable.active is True:
                self.snmpvariables.append(snmpvariable)

    def __repr__(self):
        """Return a representation of the attributes of the class.

        Args:
            None

        Returns:
            result: String representation

        """
        # Return repr
        return (
            '<{0} snmpvariables={1}>'
            ''.format(
                self.__class__.__name__,
                repr(self.snmpvariables)
            )
        )


class OIDVariable(object):
    """Variable representation for OID data for SNMP polling."""

    def __init__(self, oids=None, ip_devices=None):
        """Initialize the class.

        Args:
            oids: SNMP oids
            ip_devices: Devices that require data from oids

        Returns:
            None

        """
        # Initialize ip_devices
        if isinstance(ip_devices, str) is True:
            self.ip_devices = [ip_devices]
        elif isinstance(ip_devices, list) is True:
            self.ip_devices = ip_devices
        else:
            self.ip_devices = []

        # Initialize oids
        if isinstance(oids, str) is True:
            self.oids = [oids]
        elif isinstance(oids, list) is True:
            self.oids = oids
        else:
            self.oids = []

        # Set active
        self.active = False not in [bool(self.oids), bool(self.ip_devices)]

    def __repr__(self):
        """Return a representation of the attributes of the class.

        Args:
            None

        Returns:
            result: String representation.

        """
        # Return repr
        return (
            '<{0} active={3}, oids={1}, ip_devices={2}>'
            ''.format(
                self.__class__.__name__,
                repr(self.oids), repr(self.ip_devices), repr(self.active)
            )
        )


def _strip_non_printable(value):
    """Strip non printable characters.

    Removes any non-printable characters and adds an indicator to the string
    when binary characters are found.

    Args:
        value: the value that you wish to strip

    Returns:
        printable_value: Printable string

    """
    # Initialize key variables
    printable_value = ''

    if isinstance(value, str) is False:
        printable_value = value
    else:
        # Filter all non-printable characters
        # (note that we must use join to account for the fact that Python 3
        # returns a generator)
        printable_value = ''.join(
            [x for x in value if x.isprintable() is True])
        if printable_value != value:
            if bool(printable_value) is True:
                printable_value = '{} '.format(printable_value)
            printable_value = '{}(contains binary)'.format(printable_value)

    # Return
    return printable_value