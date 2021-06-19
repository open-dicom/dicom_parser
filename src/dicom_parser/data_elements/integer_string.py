"""
Definition of the :class:`IntegerString` class, representing a single "IS" data
element.
"""
from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation


class IntegerString(DataElement):
    #: The VR value of data elements represented by this class.
    VALUE_REPRESENTATION = ValueRepresentation.IS

    def parse_value(self, value: str) -> int:
        """
        Returns the parsed "IS" data element's value.

        Warning
        -------
        Invalid values (values raising a *TypeError* or *ValueError* when
        passed to :class:`int`) will return *None*.

        Parameters
        ----------
        value : str
            Raw "IS" data element value

        Returns
        -------
        int
            Parsed integer
        """
        try:
            return int(value)
        except (TypeError, ValueError):
            pass
