"""
Utility functions used to parse DICOM data element tags.
"""
from pydicom.tag import Tag as PydicomTag


def int_to_tag_hex(value: int) -> str:
    """
    Converts the *int* representation of tags to a *hex* string.

    Parameters
    ----------
    value : int
        Raw tag representation as integer

    Returns
    -------
    str
        Hexadecimal string representation
    """
    return format(value, "x").zfill(4)


def parse_tag(tag: PydicomTag) -> tuple:
    """
    Parses *pydicom*\'s tuple of integers into a tuple of hexadecimal strings.

    Parameters
    ----------
    tag : PydicomTag
        *pydicom*\'s tag representation

    Returns
    -------
    tuple
        Formatted tag representation
    """
    return int_to_tag_hex(tag.group), int_to_tag_hex(tag.element)
