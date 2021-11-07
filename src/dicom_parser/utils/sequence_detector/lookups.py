"""
Available lookups for various detectors.
"""
from typing import Any, Iterable


def icontains(header_value: str, rule_value: str) -> bool:
    """
    Case insensitive implementation of str-in-str lookup.

    Parameters
    ----------
    header_value : str
        String to look within.
    rule_value : str
        String to look for.

    Returns
    -------
    bool
        Whether *rule* exists in *value*
    """
    return rule_value.lower() in header_value.lower()


def is_in(header_value: Iterable, rule_value: Any) -> bool:
    """
    Checks whether *rule* exists within *value*.

    Parameters
    ----------
    value : Iterable
        An iterable of any kind
    rule : Any
        An object to look for in *value*

    Returns
    -------
    bool
        Whether *rule* exists in *value*
    """
    return rule_value in header_value if header_value else False


def not_in(header_value: Iterable, rule_value: Any) -> bool:
    """
    Checks whether *rule* doesn't exist within *value*.

    Parameters
    ----------
    value : Iterable
        An iterable of any kind
    rule : Any
        An object to look for in *value*

    Returns
    -------
    bool
        Whether *rule* doesn't exist in *value*
    """
    return rule_value not in header_value if header_value else False


def exact(header_value: Any, rule_value: Any) -> bool:
    """
    Checks whether *rule* is identical to *value*.

    Parameters
    ----------
    value : Any
        Any kind of object
    rule : Any
        Any kind of object

    Returns
    -------
    bool
        Whether *rule* is identical to *value*
    """
    return header_value == rule_value


def greater_than(header_value: int, rule_value: int) -> bool:
    return header_value > rule_value


def less_than(header_value: int, rule_value: int) -> bool:
    return header_value < rule_value


#: Lookups used to evaluate detectors' rules
LOOKUPS = {
    "icontains": icontains,
    "in": is_in,
    "not in": not_in,
    "exact": exact,
    "gt": greater_than,
    "lt": less_than,
}
