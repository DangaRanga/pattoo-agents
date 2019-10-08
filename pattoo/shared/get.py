#!/usr/bin/env python3
"""Pattoo get library."""

import os
import sys
import time
import hashlib
import yaml
import json
import urllib

# Pattoo libraries
from pattoo.shared import configuration
from pattoo.shared import log
import pattoo


def get_url_json(url):
    """Get JSON from remote URL.

    Args:
        url: URL to poll

    Returns:
        result: dict of JSON retrieved.

    """
    # Initialize key variables
    result = {}

    # Get URL
    try:
        with urllib.request.urlopen(url) as u_handle:
            try:
                result = json.loads(u_handle.read().decode())
            except:
                error = sys.exc_info()[:2]
                log_message = (
                    'Error reading JSON from URL {}: ({} {})'
                    ''.format(url, error[0], error[1]))
                log.log2info(1186, log_message)
    except:
        # Most likely no connectivity or the TCP port is unavailable
        error = sys.exc_info()[:2]
        log_message = (
            'Error contacting URL {}: ({} {})'
            ''.format(url, error[0], error[1]))
        log.log2info(1186, log_message)

    # Return
    return result
