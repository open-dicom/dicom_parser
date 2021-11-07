"""
Definition of the :class:`CodeString` class, representing a single "CS" data
element.
"""
import warnings
from enum import Enum

from dicom_parser.data_element import DataElement
from dicom_parser.utils.code_strings import (
    Modality,
    PatientPosition,
    ScanningSequence,
    SequenceVariant,
    Sex,
)
from dicom_parser.utils.value_representation import ValueRepresentation


class CodeString(DataElement):
    #: The VR value of data elements represented by this class.
    VALUE_REPRESENTATION = ValueRepresentation.CS

    #: Most code strings have a set of valid values. This dictionary checks
    #: parsed values against *Enum*\s of the valid values associated by tag.
    TAG_TO_ENUM = {
        ("0008", "0060"): Modality,
        ("0018", "5100"): PatientPosition,
        ("0018", "0020"): ScanningSequence,
        ("0018", "0021"): SequenceVariant,
        ("0010", "0040"): Sex,
    }

    @staticmethod
    def warn_invalid_code_string_value(
        exception: KeyError, enum: Enum
    ) -> None:
        """
        Displays a warning for invalid Code String (CS) values.

        Parameters
        ----------
        exception : KeyError
            The exception raised when trying to parse the invalid value
        enum : enum.Enum
            An Enum representing the element's valid values
        """
        field_name = enum.__name__
        value = exception.args[0]
        warning = f"'{value}' is not a valid {field_name} value!"
        warnings.warn(warning)

    def parse_with_enum(self, value: str, enum: Enum) -> str:
        """
        Tries to return the verbose value of a "CS" data element using the
        appropriate *Enum* (see
        :attr:`~dicom_parser.data_elements.code_string.CodeString.TAG_TO_ENUM`).

        Parameters
        ----------
        value : str
            Raw "CS" data element value
        enum : Enum
            This data element's values *Enum*

        Returns
        -------
        str
            Parsed "CS" data element value
        """
        try:
            return enum[value].value
        except KeyError as exception:
            self.warn_invalid_code_string_value(exception, enum)
            return value

    def parse_value(self, value: str) -> str:
        """
        Tries to return a parsed value using the appropriate values *Enum* (see
        :attr:`~dicom_parser.data_elements.code_string.CodeString.TAG_TO_ENUM`).

        Parameters
        ----------
        value : str
            Raw "CS" data element value

        Returns
        -------
        str
            Parsed "CS" data element value
        """
        enum = self.TAG_TO_ENUM.get(self.tag)
        if enum:
            return self.parse_with_enum(value, enum)
        return value.strip()
