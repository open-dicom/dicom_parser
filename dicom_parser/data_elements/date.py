from datetime import datetime
from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation


class Date(DataElement):
    VALUE_REPRESENTATION = ValueRepresentation.DA

    def parse_value(self, value: str) -> datetime.date:
        try:
            return datetime.strptime(value, "%Y%m%d").date()
        except ValueError:
            # If the value is not empty, raise an error indicating the data is not valid
            if value:
                raise ValueError(f"Failed to parse '{value}' into a valid date object")
            # If empty string, returns None
        except TypeError:
            # If the value is None, simply return None, else raise TypeError
            if value:
                raise
