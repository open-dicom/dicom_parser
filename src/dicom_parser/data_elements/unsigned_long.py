"""
Definition of the :class:`UnsignedLong` class, representing a single "UL" data
element.
"""
from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation


class UnsignedLong(DataElement):
    #: The VR value of data elements represented by this class.
    VALUE_REPRESENTATION = ValueRepresentation.UL
