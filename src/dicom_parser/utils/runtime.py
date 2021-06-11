import os
import platform

RUNNING_ON_WINDOWS = platform.system() == "Windows" or os.name == "nt"
