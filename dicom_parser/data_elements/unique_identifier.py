"""
Definition of the :class:`UniqueIdentifer` class, representing a single "UI"
data element.
"""

from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation


class UniqueIdentifer(DataElement):
    #: The VR value of data elements represented by this class.
    VALUE_REPRESENTATION = ValueRepresentation.UI
