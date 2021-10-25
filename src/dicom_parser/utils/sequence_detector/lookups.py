"""
Available lookups for various detectors.
"""
from typing import Iterable, Any
from dicom_parser.utils.sequence_detector.messages import ICONTAINS_TYPE_ERROR


#: Definitions of lookups used to evaluate detectors' rules
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
        Whether *rule* exists in *value*
    """
    # I guess this needs fixing. Did this because values get here in the form
    # of tuple, which raises an error even if the tuple contains a single
    # string.
    if len(value) == 1:
        value = list(value)[0]

    if not (isinstance(value, str) and isinstance(rule, str)):
        message = ICONTAINS_TYPE_ERROR.format(
            rule_type=type(rule), value_type=type(value)
        )
        raise TypeError(message)
    return rule.lower() in value.lower()


def is_in(value: Iterable, rule: Any) -> bool:
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
    return rule in value if value else False


def not_in(value: Iterable, rule: Any) -> bool:
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

    return rule not in value if value else False


def exact(value: Any, rule: Any) -> bool:
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
    print(rule, value)
    return rule == value


#: Lookups used to evaluate detectors' rules
LOOKUPS = {
    "icontains": icontains,
    "in": is_in,
    "not in": not_in,
    "exact": exact,
}
