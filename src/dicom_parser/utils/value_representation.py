"""
This file contains an *Enum* with the two-character codes of the various DICOM
value-representations (VRs).
"""
from dicom_parser.utils.choice_enum import ChoiceEnum
from dicom_parser.utils.messages import INVALID_VR


class ValueRepresentation(ChoiceEnum):
    """
    DICOM `value-representations (VRs)`_.

    .. _value-representations (VRs):
       http://northstar-www.dartmouth.edu/doc/idl/html_6.2/Value_Representations.html

    """

    AE = "Application Entity"
    AS = "Age String"
    AT = "Attribute Tag"
    CS = "Code String"
    DA = "Date"
    DS = "Decimal String"
    DT = "Date Time"
    FL = "Floating Point Single"
    FD = "Floating Point Double"
    IS = "Integer String"
    LO = "Long String"
    LT = "Long Text"
    OB = "Other Byte"
    OD = "Other Double"
    OF = "Other Float"
    OL = "Other Long"
    OV = "Other 64-bit Very Long"
    OW = "Other Word"
    PN = "Person Name"
    SH = "Short String"
    SL = "Signed Long"
    SQ = "Sequence of Items"
    SS = "Signed Short"
    ST = "Short Text"
    SV = "Signed 64-bit Very Long"
    TM = "Time"
    UC = "Unlimited Characters"
    UI = "Unique Identifer"
    UL = "Unsigned Long"
    UN = "Unknown"
    UR = "Universal Resource"
    US = "Unsigned Short"
    UT = "Unlimited Text"
    UV = "Unsigned 64-bit Very Long"


class ValueRepresentationError(Exception):
    """
    Custom execption indicating a data element has an invalid VR value.
    """


def get_value_representation(key: str) -> ValueRepresentation:
    """
    Utility function to match the VR key in *pydicom*\'s data elements
    with the appropriate *Enum* value.

    Parameters
    ----------
    key : str
        Value representation key

    Returns
    -------
    ValueRepresentation
        *Enum* value

    Raises
    ------
    ValueRepresentationError
        Invalid value representation
    """
    try:
        return ValueRepresentation[key]
    except KeyError:
        raise ValueRepresentationError(INVALID_VR.format(key=key))
