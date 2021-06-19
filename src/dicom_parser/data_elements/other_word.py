"""
Definition of the :class:`OtherWord` class, representing a single "OW" data
element.
"""
from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation


class OtherWord(DataElement):
    #: The VR value of data elements represented by this class.
    VALUE_REPRESENTATION = ValueRepresentation.OW

    def parse_value(self, value: bytes) -> list:
        """
        Returns the parsed "OW" data element value.

        Parameters
        ----------
        value : bytes
            Raw "OW" data element value

        Returns
        -------
        list
            Parsed value
        """

        return [v for v in value]
