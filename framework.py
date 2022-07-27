#!./venv/bin/python3

from __future__ import print_function
import logging
import sys
import os
import signal

class KeepAliveReporter(object):
    """
    Singleton object which reports test start to parent process
    """

    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        self._pipe = None
        print("{}({})".format(__name__.strip('_'), locals()))

    @property
    def pipe(self):
        return self._pipe

    @pipe.setter
    def pipe(self, pipe):
        if self._pipe is not None:
            raise Exception("Internal error - pipe should only be set once.")
        self._pipe = pipe

    def send_keep_alive(self, test, desc=None):
        """
        Write current test tmpdir & desc to keep-alive pipe to signal liveness
        """
        if self.pipe is None:
            # if not running forked..
            return

#        if isclass(test):
#            desc = "%s (%s)" % (desc, unittest.util.strclass(test))
#        else:
#            desc = test.id()
#
#        self.pipe.send((desc, config.vpp, test.tempdir, test.vpp.pid))

class VppDiedError(Exception):
    """exception for reporting that the subprocess has died."""

    signals_by_value = {
        v: k
        for k, v in signal.__dict__.items()
        if k.startswith("SIG") and not k.startswith("SIG_")
    }

    def __init__(self, rv=None, testcase=None, method_name=None):
        self.rv = rv
        self.signal_name = None
        self.testcase = testcase
        self.method_name = method_name

        try:
            self.signal_name = VppDiedError.signals_by_value[-rv]
        except (KeyError, TypeError):
            pass

        if testcase is None and method_name is None:
            in_msg = ""
        else:
            in_msg = " while running %s.%s" % (testcase, method_name)

        if self.rv:
            msg = "VPP subprocess died unexpectedly%s with return code: %d%s." % (
                in_msg,
                self.rv,
                " [%s]" % (self.signal_name if self.signal_name is not None else ""),
            )
        else:
            msg = "VPP subprocess died unexpectedly%s." % in_msg

        super(VppDiedError, self).__init__(msg)

class VppTestCase():
    """This subclass is a base class for VPP test cases that are implemented as
    classes. It provides methods to create and run test case.
    """

    @classmethod
    def setUpClass(cls):
        print("{}({})".format(__name__.strip('_'), locals()))

class VppDiedError():
    print("{}({})".format(__name__.strip('_'), locals()))

class KeepAliveReporter():
    print("{}({})".format(__name__.strip('_'), locals()))
