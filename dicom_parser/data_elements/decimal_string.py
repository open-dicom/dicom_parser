from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation


class DecimalString(DataElement):
    VALUE_REPRESENTATION = ValueRepresentation.DS

    def parse_value(self, value: str):
        return float(value)
