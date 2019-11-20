#!/usr/bin/env python3
"""Test the files module."""

# Standard imports
import unittest
import os
import sys

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
            os.path.abspath(os.path.join(
                os.path.abspath(os.path.join(
                        EXEC_DIR,
                        os.pardir)), os.pardir)), os.pardir)), os.pardir))

if EXEC_DIR.endswith(
        '/pattoo-agents/tests/test_pattoo_agents/bacnet/ip') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the \
"pattoo-agents/tests/test_pattoo_agents/bacnet/ip" directory. Please fix.''')
    sys.exit(2)

# Pattoo imports
from tests.libraries.configuration import UnittestConfig
from pattoo_agents.bacnet.ip.constants import PATTOO_AGENT_BACNETIPD


class TestConstants(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_constants(self):
        """Testing constants."""
        # Test agent constants
        self.assertEqual(
            PATTOO_AGENT_BACNETIPD, 'pattoo-agent-bacnetipd')


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()