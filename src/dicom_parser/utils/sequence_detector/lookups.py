"""
Available lookups for various detectors.
"""
from typing import Iterable, Any


def icontains(value: str, rule: str) -> bool:
    """
    Case insensitive implementation of str-in-str lookup.
    Parameters
    ----------
    value : str
        String to look within.
    rule : str
        String to look for.

    Returns
    -------
    bool
        Whether **rule** exists in **value**
    """
    if not (isinstance(value, str) and isinstance(rule, str)):
        raise TypeError(
            f"Unable to apply icontains lookup for value-rule pairings of types {type(value)}-{type(rule)} respectively."
        )
    return rule.lower() in value.lower()


def is_in(value: Iterable, rule: Any) -> bool:
    """
    Checks whether *rule* exists within *value*.
    Parameters
    ----------
    value : Iterable
        An iterable of any kind
    rule : Any
        An object to look for in **value**

    Returns
    -------
    bool
        Whether **rule** exists in **value**
    """
    return rule in value


def not_in(value: Iterable, rule: Any) -> bool:
    """
    Checks whether *rule* doesn't exist within *value*.
    Parameters
    ----------
    value : Iterable
        An iterable of any kind
    rule : Any
        An object to look for in **value**

    Returns
    -------
    bool
        Whether **rule** doesn't exist in **value**
    """
    return rule not in value


#: Lookups used in to evaluate detectors' rules
LOOKUPS = {"icontains": icontains, "in": is_in, "not in": not_in}
