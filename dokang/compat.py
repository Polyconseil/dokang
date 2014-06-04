# -*- coding: utf-8 -*-
# Copyright (c) 2011-2014 Polyconseil SAS. All rights reserved.
"""Python 2 compatibility layer."""

import sys

PY2 = sys.version[0] == '2'

# pylint: disable=redefined-builtin, invalid-name, import-error, unused-import, no-name-in-module
if PY2:
    from ConfigParser import SafeConfigParser as ConfigParser
else:
    from configparser import ConfigParser
