"""
Definition of the :class:`AgeString` class, representing a single "AS" data
element.
"""
from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation


class AgeString(DataElement):
    #: The VR value of data elements represented by this class.
    VALUE_REPRESENTATION = ValueRepresentation.AS

    # N_IN_YEAR is used in order to convert the AgeString value to a
    # standard format of a floating point number representing years.
    N_IN_YEAR = {"Y": 1, "M": 12, "W": 52.1429, "D": 365.2422}

    def parse_value(self, value: str) -> float:
        """
        Converts an Age String element's representation of age into a *float*
        representing years.

        Parameters
        ----------
        value : str
            Age String value

        Returns
        -------
        float
            Age in years
        """
        try:
            duration = float(value[:-1])
            units = value[-1]
            return duration / self.N_IN_YEAR[units]

        # If empty or invalid value, return None
        except ValueError:
            pass
