"""
Definition of the :class:`DecimalString` class, representing a single "DS" data
element.
"""
from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation


class DecimalString(DataElement):
    #: The VR value of data elements represented by this class.
    VALUE_REPRESENTATION = ValueRepresentation.DS

    def parse_value(self, value: str) -> float:
        """
        Returns the parsed "DS" data element's value.

        Warning
        -------
        Invalid values (values raising a *TypeError* or *ValueError* when
        passed to :class:`float`) will return *None*.

        Parameters
        ----------
        value : str
            Raw "DS" data element value

        Returns
        -------
        float
            Parsed decimal
        """
        try:
            return float(value)
        except (TypeError, ValueError):
            pass
