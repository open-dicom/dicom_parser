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
        An iterable of some
    rule : Any
        [description]

    Returns
    -------
    bool
        [description]
    """
    return rule in value


#: Lookups used in to evaluate detectors' rules
LOOKUPS = {"icontains": icontains}
