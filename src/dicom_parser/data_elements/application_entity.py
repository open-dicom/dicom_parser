"""
Definition of the :class:`ApplicationEntity` class, representing a single "AE"
data element.
"""
from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation


class ApplicationEntity(DataElement):
    #: The VR value of data elements represented by this class.
    VALUE_REPRESENTATION = ValueRepresentation.AE
