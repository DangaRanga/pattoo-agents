#!/usr/bin/env python3
"""Pattoo Agent class.

Description:

    This script:
        1) Processes a variety of information from agents
        2) Posts the data using HTTP to a server listed
           in the configuration file

"""
# Standard libraries
import os
import json

# pip3 libraries
import requests

# Pattoo libraries
from pattoo.shared import log
from pattoo.shared import data as lib_data
from pattoo.shared import agent as lib_agent
from pattoo.shared import configuration


class Data(object):
    """Pattoo agent that gathers data."""

    def __init__(self, _data):
        """Initialize the class.

        Args:
            _data: Data to post

        Returns:
            None

        """
        # Initialize key variables
        self._post_data = _data

        # Get the agent_name
        if 'agent_program' in self._post_data:
            self._agent_program_post = self._post_data['agent_program']
        else:
            self._agent_program_post = ''

        # Get the agent ID
        config = configuration.Config()
        agent_id = lib_agent.get_agent_id(self._agent_program_post)

        # Get posting URL
        self._url = config.api_server_url(agent_id)

        # Get the agent cache directory
        self._cache_dir = config.agent_cache_directory(
            self._agent_program_post)

        # All cache files created by this agent will end with this suffix.
        devicehash = lib_data.hashstring(
            self._post_data['agent_hostname'], sha=1)
        self._cache_filename_suffix = '{}_{}.json'.format(agent_id, devicehash)

    def post(self, save=True, data=None):
        """Post data to central server.

        Args:
            save: When True, save data to cache directory if postinf fails
            data: Data to post. If None, then uses self._post_data (
                Used for testing and cache purging)

        Returns:
            success: True: if successful

        """
        # Initialize key variables
        success = False
        response = False
        timestamp = self._post_data['timestamp']

        # Create data to post
        if data is None:
            data2post = self._post_data
        else:
            data2post = data

        # Post data save to cache if this fails
        try:
            result = requests.post(self._url, json=data2post)
            response = True
        except:
            if save is True:
                # Create a unique very long filename to reduce risk of
                filename = '{}/{}_{}'.format(
                    self._cache_dir, timestamp, self._cache_filename_suffix)

                # Save data
                with open(filename, 'w') as f_handle:
                    json.dump(data2post, f_handle)
            else:
                # Proceed normally if there is a failure.
                # This will be logged later
                pass

        # Define success
        if response is True:
            if result.status_code == 200:
                success = True

        # Log message
        if success is True:
            log_message = (
                'Agent "{}" successfully contacted server {}'
                ''.format(self._agent_program_post, self._url))
            log.log2info(1027, log_message)
        else:
            log_message = (
                'Agent "{}" failed to contact server {}'
                ''.format(self._agent_program_post, self._url))
            log.log2warning(1028, log_message)

        # Return
        return success

    def purge(self):
        """Purge data from cache by posting to central server.

        Args:
            None

        Returns:
            success: "True: if successful

        """
        # Initialize key variables
        agent_id = self._post_data['agent_id']

        # Add files in cache directory to list only if they match the
        # cache suffix
        all_filenames = [filename for filename in os.listdir(
            self._cache_dir) if os.path.isfile(
                os.path.join(self._cache_dir, filename))]
        filenames = [
            filename for filename in all_filenames if filename.endswith(
                self._cache_filename_suffix)]

        # Read cache file
        for filename in filenames:
            # Only post files for our own UID value
            if agent_id not in filename:
                continue

            # Get the full filepath for the cache file and post
            filepath = os.path.join(self._cache_dir, filename)
            with open(filepath, 'r') as f_handle:
                try:
                    data = json.load(f_handle)
                except:
                    # Log removal
                    log_message = (
                        'Error reading previously cached agent data file {} '
                        'for agent {}. May be corrupted.'
                        ''.format(filepath, self._agent_program_post))
                    log.log2die(1064, log_message)

            # Post file
            success = self.post(save=False, data=data)

            # Delete file if successful
            if success is True:
                os.remove(filepath)

                # Log removal
                log_message = (
                    'Purging cache file {} after successfully '
                    'contacting server {}'
                    ''.format(filepath, self._url))
                log.log2info(1029, log_message)
