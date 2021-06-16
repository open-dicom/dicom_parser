"""
Definition of the :class:`FloatingPointSingle` class, representing a single
"FL" data element.
"""
from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation


class FloatingPointSingle(DataElement):
    #: The VR value of data elements represented by this class.
    VALUE_REPRESENTATION = ValueRepresentation.FL
