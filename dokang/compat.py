# -*- coding: utf-8 -*-
# Copyright (c) Polyconseil SAS. All rights reserved.
"""Python 2 compatibility layer."""

from __future__ import print_function

import os
import sys

PY2 = sys.version[0] == '2'

# pylint: disable=redefined-builtin, invalid-name, import-error, unused-import, no-name-in-module
if PY2:
    from ConfigParser import SafeConfigParser as ConfigParser

    def print_to_stdout(unicode_string):
        print(unicode_string.encode(sys.stdout.encoding))
else:
    from configparser import ConfigParser

    def print_to_stdout(string):
        string += os.linesep
        sys.stdout.buffer.write(string.encode(sys.stdout.encoding))
