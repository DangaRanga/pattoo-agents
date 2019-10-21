#!/usr/bin/env python3
"""Pattoo agent data cache ingester.

Used to add data to backend database

"""

# Standard libraries
import sys
import os
from pprint import pprint

# Try to create a working PYTHONPATH
_BIN_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
_ROOT_DIRECTORY = os.path.abspath(os.path.join(_BIN_DIRECTORY, os.pardir))
if _BIN_DIRECTORY.endswith('/pattoo-agents/bin') is True:
    sys.path.append(_ROOT_DIRECTORY)
else:
    print(
        'This script is not installed in the "pattoo-agents/bin" directory. '
        'Please fix.')
    sys.exit(2)

# Pattoo libraries
from pattoo_shared.constants import PATTOO_API_AGENT_EXECUTABLE
from pattoo_shared.configuration import Config
from pattoo_shared import files
from pattoo_shared import converter
from pattoo_shared.variables import AgentPolledData


def main():
    """Ingest data.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    result = []

    # Read data from cache
    config = Config()
    directory = config.agent_cache_directory(PATTOO_API_AGENT_EXECUTABLE)
    directory_data = files.read_json_files(directory, die=False)

    # Read data into a list of tuples
    # [(filepath, AgentPolledData obj), (filepath, AgentPolledData obj) ...]
    for filepath, json_data in directory_data:
        agentdata = converter.convert(json_data)
        if isinstance(agentdata, AgentPolledData) is True:
            if agentdata.active is True:
                result.append((filepath, agentdata))
                break

    # Show results prior to writing code to add to database
    pprint(result)


if __name__ == '__main__':
    main()
