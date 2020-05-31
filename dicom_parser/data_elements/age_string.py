from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation


class AgeString(DataElement):
    VALUE_REPRESENTATION = ValueRepresentation.AS

    # N_IN_YEAR is used in order to convert the AgeString value to a
    # standard format of a floating point number representing years.
    N_IN_YEAR = {"Y": 1, "M": 12, "W": 52.1429, "D": 365.2422}

    def parse_value(self, value) -> float:
        duration = float(value[:-1])
        units = value[-1]
        return duration / self.N_IN_YEAR[units]
