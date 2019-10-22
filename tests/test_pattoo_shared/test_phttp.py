#!/usr/bin/env python3
"""Test the phttp module."""

# Standard imports
import unittest
import os
import sys


# Try to create a working PYTHONPATH
EXEC_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
ROOT_DIRECTORY = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(EXEC_DIRECTORY, os.pardir)), os.pardir))
if EXEC_DIRECTORY.endswith('/pattoo-agents/tests/test_pattoo_shared') is True:
    sys.path.append(ROOT_DIRECTORY)
else:
    print('''\
This script is not installed in the "pattoo-agents/tests/test_pattoo_shared" \
directory. Please fix.''')
    sys.exit(2)

# Pattoo imports
from pattoo_shared import phttp
from pattoo_shared.configuration import Config
from tests.dev import unittest_setup


class TestPost(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test___init__(self):
        """Testing method / function __init__."""
        pass

    def test_post(self):
        """Testing method / function post."""
        pass

    def test_purge(self):
        """Testing method / function purge."""
        pass


class TestPassiveAgent(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test___init__(self):
        """Testing method / function __init__."""
        pass

    def test_relay(self):
        """Testing method / function relay."""
        pass

    def test_get(self):
        """Testing method / function get."""
        pass


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    unittest_setup.ready()

    # Do the unit test
    unittest.main()
