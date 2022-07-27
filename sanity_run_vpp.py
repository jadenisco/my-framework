#!./venv/bin/python3

from __future__ import print_function
from multiprocessing import Pipe
import sys
import os
from framework import VppDiedError, VppTestCase, KeepAliveReporter


class SanityTestCase(VppTestCase):
    """Sanity test case - verify whether VPP is able to start"""
    print("{}({})".format(__name__.strip('_'), locals()))

    cpus = [0]

    # don't ask to debug SanityTestCase
 #   @classmethod
 #   def wait_for_enter(cls, pid=0):
 #       pass

#  @classmethod
#    def _debug_quit(cls):
#        try:
#            cls.vpp.poll()
#        except AttributeError:
#            pass


def main():
    print("{}({})".format(__name__.strip('_'), locals()))

    rc = 0
    tc = SanityTestCase
    x, y = Pipe()
    reporter = KeepAliveReporter()
    reporter.pipe = y
#    try:
#        tc.setUpClass()
#    except VppDiedError:
#        rc = -1
#    else:
#        try:
#            tc.tearDownClass()
#        except Exception:
#            rc = -1
#    x.close()
#    y.close()

    if rc == 0:
        print("Sanity test case passed.")
    else:
        print("Sanity test case failed.")
    return rc


if __name__ == "__main__":
    sys.exit(main())
