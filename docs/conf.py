# In case the package has not been installed, add it to PYTHONPATH.
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from blease.doc.sphinxbaseconf import *

from dokang.version import VERSION
project = "Dokang"
version = VERSION
release = version
