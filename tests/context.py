import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import nmdmail  # noqa: F401, E402
from nmdmail import cli  # noqa: F401, E402
