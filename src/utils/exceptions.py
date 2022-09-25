# -*- coding: utf-8 -*-
"""
Definitions for specific exception handling.
"""

#  standard imports
# third party imports
# custom imports


class DatabaseConnectionException(Exception):
    """Raised when the database cannot be reached."""
    pass


class DataNotFoundException(Exception):
    """Generic exception for not finding data by query"""
    def __init__(self, msg, original_exception):
        super(DataNotFoundException, self).__init__(msg + (": %s" % original_exception))
        self.original_exception = original_exception