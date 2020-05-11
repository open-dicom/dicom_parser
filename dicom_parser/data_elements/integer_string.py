from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation


class IntegerString(DataElement):
    VALUE_REPRESENTATION = ValueRepresentation.IS

    def parse_value(self, value: str):
        return int(value)
