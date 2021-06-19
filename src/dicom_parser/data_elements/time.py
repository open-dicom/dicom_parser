"""
Definition of the :class:`Time` class, representing a single "TM" data element.
"""
from datetime import datetime

from dicom_parser.data_element import DataElement
from dicom_parser.data_elements.messages import TIME_PARSING_FAILURE
from dicom_parser.utils.value_representation import ValueRepresentation


class Time(DataElement):
    #: The VR value of data elements represented by this class.
    VALUE_REPRESENTATION = ValueRepresentation.TM

    def parse_value(self, value: str) -> datetime.time:
        """
        Converts the DICOM standard's time string representation into an
        instance of Python's :class:`datetime.time`.


        Parameters
        ----------
        value : str
            Raw "TM" data element value

        Returns
        -------
        datetime.time
            Parsed time

        Raises
        ------
        ValueError
            Failure to parse time from raw value
        """
        try:
            # Try to parse according to the default time representation
            return datetime.strptime(value, "%H%M%S.%f").time()
        except ValueError:
            # If the value is not empty, try to parse with the fractional part
            if value:
                try:
                    return datetime.strptime(value, "%H%M%S").time()
                except ValueError:
                    message = TIME_PARSING_FAILURE.format(value=value)
                    raise ValueError(message)
            # If the value is empty string, simply return None
        except TypeError:
            # If the value is empty, simply return None, else raise TypeError
            if value or value is False:
                raise
