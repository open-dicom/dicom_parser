"""
Runtime information to check for conditionally supported functionality.
"""
import os
import platform

#: Whether the running OS is Windows or not.
RUNNING_ON_WINDOWS = platform.system() == "Windows" or os.name == "nt"
