#!/usr/bin/env python3
"""Pattoo helper for the Linux _data.

Description:

    Uses Python2 to be compatible with most Linux systems


"""
# Standard libraries
from collections import defaultdict
from copy import deepcopy
import socket
import hashlib


# Pattoo libraries
from pattoo.agents.os import language
from pattoo import log
from pattoo import times
from pattoo import agent as agent_lib
from pattoo.variables import DataVariable, DATA_INT, DATA_STRING


class Data(object):
    """Pattoo agent that gathers data."""

    def __init__(self, agent_program, polled_data, device_polled):
        """Initialize the class.

        Args:
            agent_program: Name of agent program
            polled_data: DataVariableList object
            device_polled: Name of device polled

        Returns:
            None

        """
        # Initialize key variables
        self._data = defaultdict(lambda: defaultdict(dict))
        agent_id = agent_lib.get_agent_id(agent_program)
        self._lang = language.Agent(agent_program)
        self._polled_data = polled_data

        # Get devicename
        self._devicename = socket.getfqdn()

        # Add timestamp
        self._data['timestamp'] = times.normalized_timestamp()
        self._data['agent_id'] = agent_id
        self._data['agent_program'] = agent_program
        self._data['agent_hostname'] = self._devicename
        self._data['devices'] = defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: defaultdict())))

    def _process(self):
        """Return the name of the _data.

        Args:
            None

        Returns:
            value: Name of agent

        """
        # Intitialize key variables
        timeseries = defaultdict(lambda: defaultdict(dict))
        timefixed = defaultdict(lambda: defaultdict(dict))

        # Get information from data
        for item in self._polled_data:
            data_tuple = (item.data_index. item.value)
            if item.data_type == DATA_STRING:
                if item.data_label in timefixed:
                    timefixed['data'].append(data_tuple)
                else:
                    timefixed[item.data_label]['base_type'] = item.data_type
                    timefixed['data'] = data_tuple
            else:
                if item.data_label in timeseries:
                    timeseries['data'].append(data_tuple)
                else:
                    timeseries[item.data_label]['base_type'] = item.data_type
                    timeseries['data'] = data_tuple

        # Return
        return (timeseries, timefixed)

    def populate(self, data_in):
        """Populate data for agent to eventually send to server.

        Args:
            data_in: dict of datapoint values from agent
            timeseries: TimeSeries data if True

        Returns:
            None

        """
        # Initialize data
        data = deepcopy(data_in)

        # Validate base_type
        if len(data) != 1 or isinstance(data, defaultdict) is False:
            log_message = 'Agent data "{}" is invalid'.format(data)
            log.log2die(1025, log_message)

        # Get a description to use for label value
        for label in data.keys():
            description = self._lang.label_description(label)
            data[label]['description'] = description
            break

        # Add data to appropriate self._data key
        if data[label]['base_type'] is not None:
            self._data['devices'][self._devicename]['timeseries'].update(data)
        else:
            self._data['devices'][self._devicename]['timefixed'].update(data)

    def data(self):
        """Return that that should be posted.

        Args:
            None

        Returns:
            None

        """
        # Return
        return self._data


def encode(value):
    """Encode string value to utf-8.

    Args:
        value: String to encode

    Returns:
        result: encoded value

    """
    # Initialize key variables
    result = value

    # Start decode
    if value is not None:
        if isinstance(value, str) is True:
            result = value.encode()

    # Return
    return result


def decode(value):
    """Decode utf-8 value to string.

    Args:
        value: String to decode

    Returns:
        result: decoded value

    """
    # Initialize key variables
    result = value

    # Start decode
    if value is not None:
        if isinstance(value, bytes) is True:
            result = value.decode('utf-8')

    # Return
    return result


def hashstring(string, sha=256, utf8=False):
    """Create a UTF encoded SHA hash string.

    Args:
        string: String to hash
        length: Length of SHA hash
        utf8: Return utf8 encoded string if true

    Returns:
        result: Result of hash

    """
    # Initialize key variables
    listing = [1, 224, 384, 256, 512]

    # Select SHA type
    if sha in listing:
        index = listing.index(sha)
        if listing[index] == 1:
            hasher = hashlib.sha1()
        elif listing[index] == 224:
            hasher = hashlib.sha224()
        elif listing[index] == 384:
            hasher = hashlib.sha512()
        elif listing[index] == 512:
            hasher = hashlib.sha512()
        else:
            hasher = hashlib.sha256()

    # Encode the string
    hasher.update(bytes(string.encode()))
    device_hash = hasher.hexdigest()
    if utf8 is True:
        result = device_hash.encode()
    else:
        result = device_hash

    # Return
    return result


def is_numeric(val):
    """Check if argument is a number.

    Args:
        val: String to check

    Returns:
        True if a number

    """
    # Try edge case
    if val is True:
        return False
    if val is False:
        return False

    # Try conversions
    try:
        float(val)
        return True
    except ValueError:
        return False
    except TypeError:
        return False
    except:
        return False


def named_tuple_to_dv(
        values, data_label=None, data_type=DATA_INT):
    """Convert a named tuple to a list of DataVariable objects.

    Args:
        values: Named tuple
        data_label: data_label
        data_type: Data type

    Returns:
        result: List of DataVariable

    """
    # Get data
    data_dict = values._asdict()
    result = []

    # Cycle through results
    for data_index, value in data_dict.items():
        _dv = DataVariable(
            value=value,
            data_label=data_label,
            data_index=data_index,
            data_type=data_type)
        result.append(_dv)

    # Return
    return result
