"""
Definition of the :class:`FloatingPointDouble` class, representing a single
"FD" data element.
"""
from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation


class FloatingPointDouble(DataElement):
    #: The VR value of data elements represented by this class.
    VALUE_REPRESENTATION = ValueRepresentation.FD
