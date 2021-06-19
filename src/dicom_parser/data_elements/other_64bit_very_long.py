"""
Definition of the :class:`Other64bitVeryLong` class, representing a single "OV"
data element.
"""
from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation


class Other64bitVeryLong(DataElement):
    #: The VR value of data elements represented by this class.
    VALUE_REPRESENTATION = ValueRepresentation.OV
