"""
Available operators for various detectors.
"""
from typing import Iterable


def operator_any(rules: list) -> bool:
    """
    An implementation of the **any** function, suited for the detection of
    scanning sequences.

    Parameters
    ----------
    rules : list
        List of booleans describing rules for a detector

    Returns
    -------
    bool
        True if any of the rules is True, False otherwise
    """
    return any(rules) if isinstance(rules, Iterable) else bool(rules)


def operator_all(rules: list) -> bool:
    """
    An implementation of the **all** function, suited for the detection of
    scanning sequences.

    Parameters
    ----------
    rules : list
        List of booleans describing rules for a detector

    Returns
    -------
    bool
        True if all of the rules are True, False otherwise
    """
    return all(rules) if isinstance(rules, Iterable) else bool(rules)


#: Operators used to evaluate detectors' rules
OPERATORS = {"any": operator_any, "all": operator_all}
