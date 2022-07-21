#!/usr/bin/env python3
import logging

class VppTestCase():
    """This subclass is a base class for VPP test cases that are implemented as
    classes. It provides methods to create and run test case.
    """

    @classmethod
    def set_debug_flags(cls, d):
        logging.debug("{}({})".format(__name__.strip('_'), locals()))

    @classmethod
    def setUpClass(cls):
        logging.debug("{}({})".format(__name__.strip('_'), locals()))

