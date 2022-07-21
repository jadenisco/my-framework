#!/usr/bin/env python3
import sys
import argparse
import logging

from framework import VppTestCase
class SanityTestCase(VppTestCase):
    """ Sanity test case - verify whether VPP is able to start """

    # don't ask to debug SanityTestCase
    @classmethod
    def wait_for_enter(cls, pid=0):
        logging.debug("wait_for_event()")

    @classmethod
    def _debug_quit(cls):
        logging.debug("_debug_quit()")

def main():
    logging.debug("{}({})".format(__name__.strip('_'), locals()))

    # tc = SanityTestCase


if __name__ == '__main__':

    main_parser = argparse.ArgumentParser(
        prog='covid-forms',
        description='This utility is used to experiment with the VPP test framework.',
        epilog='See "%(prog)s help COMMAND" for help on a specific command.')
    main_parser.add_argument('--debug', '-d', action='count', help='Print debug output')

    main_args = main_parser.parse_args()

    if main_args.debug:
        logging.basicConfig(level=logging.DEBUG)


    sys.exit(main())
