"""
Ry Stats Lang — Python API

This module defines the public Python-facing API for Ry.
Internal modules and runtime details are intentionally hidden.
"""

# Core
from .core import *
from .Modules.TypeConversion import *
from .Modules.Inspection import *
from .Modules.Access import *

# I/O
from .Modules.IOLayer import *

# Math & Stats
from .Modules.MathBasic import *
from .Modules.MathTransforms import *
from .Modules.Distributions import *

# Data
from .Modules.DataManipulation import *

# Utilities
from .Modules.Strings import *
from .Modules.DatetimeUtils import *

# Plotting
from .Modules.PlottingCore import *
from .Modules.PlottingStyle import *

# Modeling
from .Modules.Modeling import *
from .Modules.Optimization import *
from .Modules.StatisticalTests import *

# Language Utilities
from .Modules.ProgrammingUtils import *
from .Modules.SystemEnv import *
from .Modules.RyExtensions import *


__all__ = [ name for name, obj in globals().items()
            if callable(obj) and not name.startswith("_")  ] # type: ignore