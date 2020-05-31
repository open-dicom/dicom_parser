from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation


class ApplicationEntity(DataElement):
    VALUE_REPRESENTATION = ValueRepresentation.AE
