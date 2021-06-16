"""
Definition of the :class:`UnlimitedCharacters` class, representing a single
"UC" data element.
"""
from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation


class UnlimitedCharacters(DataElement):
    #: The VR value of data elements represented by this class.
    VALUE_REPRESENTATION = ValueRepresentation.UC
