# -*- coding: utf-8 -*-


class CafeNotFoundException(Exception):
    """
    Exception raised when url was not given.
    """

    def __init__(self, msg=u'Cafe Not Found'):
        self.msg = msg

    def __str__(self):
        return str(self.msg)