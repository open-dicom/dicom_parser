from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation


class OtherWord(DataElement):
    VALUE_REPRESENTATION = ValueRepresentation.OW

    def parse_value(self, value: bytes) -> list:
        return [v for v in value]
