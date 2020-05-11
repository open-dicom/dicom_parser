from datetime import datetime
from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation


class Time(DataElement):
    VALUE_REPRESENTATION = ValueRepresentation.TM

    def parse_value(self, value: str) -> datetime.time:
        try:
            # Try to parse according to the default time representation
            return datetime.strptime(value, "%H%M%S.%f").time()
        except ValueError:
            # If the value is not empty, try to parse with the fractional part
            if value:
                try:
                    return datetime.strptime(value, "%H%M%S").time()
                except ValueError:
                    raise ValueError(
                        f"Failed to parse '{value}' into a valid time object!"
                    )
            # If the value is empty string, simply return None
        except TypeError:
            # If the value is empty, simply return None, else raise TypeError
            if value:
                raise
