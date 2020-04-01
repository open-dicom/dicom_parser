"""
This file contains an `Enum <https://docs.python.org/3/library/enum.html>`_ with the two-character codes of the
various `DICOM <https://en.wikipedia.org/wiki/DICOM>`__
`value-representations (VRs) <http://northstar-www.dartmouth.edu/doc/idl/html_6.2/Value_Representations.html>`_
(also see `here <http://dicom.nema.org/medical/dicom/current/output/chtml/part05/sect_6.2.html>`_)
for header `data elements <http://northstar-www.dartmouth.edu/doc/idl/html_6.2/DICOM_Attributes.html>`_.

"""

from dicom_parser.utils.choice_enum import ChoiceEnum


class ValueRepresentation(ChoiceEnum):
    """
    DICOM `value-representations (VRs)
    <http://northstar-www.dartmouth.edu/doc/idl/html_6.2/Value_Representations.html>`_.

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


INVALID_VR_MESSAGE = (
    "{key} is not a valid DICOM data element value representation (VR)!"
)


class ValueRepresentationError(Exception):
    pass


def get_value_representation(key: str) -> ValueRepresentation:
    try:
        return ValueRepresentation[key]
    except KeyError:
        raise ValueRepresentationError(INVALID_VR_MESSAGE.format(key=key))
