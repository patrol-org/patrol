# This file is part of patrol, fork of range.
# License: GNU GPL version 3, see the file "AUTHORS" for details.

"""Shared objects contain singletons for shared use."""

from __future__ import (absolute_import, division, print_function)


class CLIAware(object):  # pylint: disable=too-few-public-methods
    """Subclass this to gain access to the global "CLI" object."""
    @staticmethod
    def cli_set(cli):
        CLIAware.cli = cli


class SettingsAware(object):  # pylint: disable=too-few-public-methods
    """Subclass this to gain access to the global "SettingObject" object."""
    @staticmethod
    def settings_set(settings):
        SettingsAware.settings = settings
