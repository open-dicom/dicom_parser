"""
Definition of the :class:`Date` class, representing a single "DA" data element.
"""
from datetime import datetime

from dicom_parser.data_element import DataElement
from dicom_parser.data_elements.messages import DATE_PARSING_FAILURE
from dicom_parser.utils.value_representation import ValueRepresentation


class Date(DataElement):
    #: The VR value of data elements represented by this class.
    VALUE_REPRESENTATION = ValueRepresentation.DA

    def parse_value(self, value: str) -> datetime.date:
        """
        Converts the DICOM standard's date string representation into an
        instance of Python's :class:`datetime.date`.


        Parameters
        ----------
        value : str
            Raw "DA" data element value

        Returns
        -------
        datetime.date
            Parsed date

        Raises
        ------
        ValueError
            Failure to parse date from raw value
        """
        try:
            return datetime.strptime(value, "%Y%m%d").date()
        except ValueError:
            # If the value is not empty, raise an error indicating the data is
            # not valid
            if value:
                message = DATE_PARSING_FAILURE.format(value=value)
                raise ValueError(message)
            # If empty string, returns None
        except TypeError:
            # If the value is None, simply return None, else raise TypeError
            if value:
                raise
