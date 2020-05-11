import warnings

from dicom_parser.data_element import DataElement
from dicom_parser.utils.code_strings import (
    Modality,
    Sex,
    PatientPosition,
    ScanningSequence,
    SequenceVariant,
)
from dicom_parser.utils.value_representation import ValueRepresentation
from enum import Enum


class CodeString(DataElement):
    VALUE_REPRESENTATION = ValueRepresentation.CS
    TAG_TO_ENUM = {
        ("0008", "0060"): Modality,
        ("0018", "5100"): PatientPosition,
        ("0018", "0020"): ScanningSequence,
        ("0018", "0021"): SequenceVariant,
        ("0010", "0040"): Sex,
    }

    def warn_invalid_code_string_value(self, exception: KeyError, enum: Enum) -> None:
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
        if warning not in self.warnings:
            self.warnings.append(warning)

    def parse_with_enum(self, value: str, enum: Enum):
        try:
            return enum[value].value
        except KeyError as exception:
            self.warn_invalid_code_string_value(exception, enum)
            return value

    def parse_value(self, value: str) -> str:
        enum = self.TAG_TO_ENUM.get(self.tag)
        if enum:
            return self.parse_with_enum(value, enum)
        return value
