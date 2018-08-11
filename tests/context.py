""" provides context for tests

This allows us to use the modules from the main project without reinstalling
the package every time the code changes.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..')))
