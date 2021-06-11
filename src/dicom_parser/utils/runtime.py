"""
Runtime information to check for conditionally supported functionality.
"""
import platform


def is_windows() -> bool:
    """
    Checks whether the running OS is Windows or not.

    Returns
    -------
    bool
        Platform is Windows
    """
    return platform.system() == "Windows"
