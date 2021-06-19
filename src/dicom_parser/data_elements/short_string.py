"""
Definition of the :class:`ShortString` class, representing a single "SH" data
element.
"""
from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation


class ShortString(DataElement):
    #: The VR value of data elements represented by this class.
    VALUE_REPRESENTATION = ValueRepresentation.SH
