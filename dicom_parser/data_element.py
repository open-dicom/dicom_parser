"""
A wrapper around pydicom_'s :class:`~pydicom.dataelem.DataElement` class.

.. _pydicom: https://github.com/pydicom/pydicom

"""
import pandas as pd
import re

from dicom_parser.utils.parse_tag import parse_tag
from dicom_parser.utils.value_representation import ValueRepresentation
from pydicom.dataelem import DataElement as PydicomDataElement


class DataElement:
    VALUE_REPRESENTATION: ValueRepresentation = None
    PRIVATE_ELEMENT_DESCRIPTION_PATTERN = r"\[(.*)\]|Private Creator"

    def __init__(self, raw: PydicomDataElement):
        self.raw: PydicomDataElement = raw
        self.tag: tuple = parse_tag(self.raw.tag)
        self.keyword: str = self.parse_keyword()
        self.value_multiplicity: int = self.raw.VM
        self.description: str = self.raw.description()

        self._value = None
        self.warnings = []

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.to_series().to_string()

    def get_private_element_keyword(self) -> str:
        pattern = self.PRIVATE_ELEMENT_DESCRIPTION_PATTERN
        description = self.raw.description()
        private_element_description = re.findall(pattern, description)
        if private_element_description:
            keyword = private_element_description[0]
            if " " in keyword:
                return keyword.title().replace(" ", "")
            return keyword
        return ""

    def parse_keyword(self):
        if self.raw.keyword == "":
            return self.get_private_element_keyword()
        return self.raw.keyword

    def parse_value(self, value):
        if isinstance(value, bytes):
            try:
                return value.decode("utf-8").strip()
            except UnicodeDecodeError:
                pass
        return value

    def parse_values(self):
        if self.value_multiplicity > 1:
            return [self.parse_value(value) for value in self.raw.value]
        return self.parse_value(self.raw.value)

    def to_dict(self) -> dict:
        return {
            "tag": self.tag,
            "keyword": self.keyword,
            "value_representation": self.VALUE_REPRESENTATION.value,
            "value_multiplicity": self.value_multiplicity,
            "value": self.value,
        }

    def to_series(self) -> pd.Series:
        d = self.to_dict()
        return pd.Series(d)

    @property
    def value(self):
        if self._value is None:
            self._value = self.parse_values()
        return self._value

    @property
    def is_private(self) -> bool:
        pattern = self.PRIVATE_ELEMENT_DESCRIPTION_PATTERN
        description = self.raw.description()
        return bool(re.match(pattern, description))

    @property
    def is_public(self) -> bool:
        return not self.is_private
