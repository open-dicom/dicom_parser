"""
Definition of the :class:`OtherByte` class, representing a single "OB" data
element.
"""
from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation


class OtherByte(DataElement):
    #: The VR value of data elements represented by this class.
    VALUE_REPRESENTATION = ValueRepresentation.OB
