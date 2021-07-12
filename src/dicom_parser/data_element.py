"""
Definition of the :class:`DataElement` class.
"""
import re
from typing import Any

from pydicom.dataelem import DataElement as PydicomDataElement

from dicom_parser.utils import parse_tag, requires_pandas
from dicom_parser.utils.value_representation import ValueRepresentation


class DataElement:
    """
    A wrapper around pydicom_'s :class:`~pydicom.dataelem.DataElement` class.
    This is a parent class for the data elements defined in
    :mod:`~dicom_parser.data_elements`.

    .. _pydicom: https://github.com/pydicom/pydicom
    """

    VALUE_REPRESENTATION: ValueRepresentation = None
    PRIVATE_ELEMENT_DESCRIPTION_PATTERN: str = r"\[(.*)\]|Private Creator"

    def __init__(self, raw: PydicomDataElement):
        """
        Initialize a new :class:`DataElement` instance.

        Parameters
        ----------
        raw : PydicomDataElement
            pydicom's data element
        """
        self.raw: PydicomDataElement = raw
        self.tag: tuple = parse_tag(self.raw.tag)
        self.keyword: str = self.parse_keyword()
        self.value_multiplicity: int = self.raw.VM
        self.description: str = self.raw.description()

        self._value = None
        self.warnings = []

    def __repr__(self) -> str:
        """
        Return the representation of this instance.

        Returns
        -------
        str
            This instance's string representation
        """
        return self.__str__()

    def __str__(self) -> str:
        """
        Return the string representation of this instance.

        Returns
        -------
        str
            This instance's string representation
        """
        try:
            return self.to_series().to_string()
        except ImportError:
            return str(self.raw)

    def get_private_element_keyword(self) -> str:
        """
        Returns the keyword of private data elements if it can be extracted.

        Returns
        -------
        str
            Private data element keyword
        """
        pattern = self.PRIVATE_ELEMENT_DESCRIPTION_PATTERN
        description = self.raw.description()
        private_element_description = re.findall(pattern, description)
        if private_element_description:
            keyword = private_element_description[0]
            if " " in keyword:
                return keyword.title().replace(" ", "")
            return keyword
        return ""

    def parse_keyword(self) -> str:
        """
        Returns the keyword for this instance.

        Returns
        -------
        str
            This instance's keyword
        """
        if self.raw.keyword == "":
            return self.get_private_element_keyword()
        return self.raw.keyword

    def parse_value(self, value: Any) -> Any:
        """
        Default :meth:`parse_value` method that simply decodes the raw value if
        it's in bytes. This method is meant to be overridden by subclasses.

        Parameters
        ----------
        value : Any
            This instance's raw value

        Returns
        -------
        Any
            This instance's parsed value
        """
        # pylint: disable=no-self-use
        if isinstance(value, bytes):
            try:
                return value.decode("utf-8").strip()
            except UnicodeDecodeError:
                pass
        return value

    def parse_values(self) -> Any:
        """
        Return the parsed value or values of this instance.

        Returns
        -------
        Any
            This instance's parsed value or values
        """
        if self.value_multiplicity > 1:
            return tuple(self.parse_value(value) for value in self.raw.value)
        return self.parse_value(self.raw.value)

    def to_dict(self) -> dict:
        """
        Create a dictionary representation of this instance.

        Returns
        -------
        dict
            This instance as a dictionary
        """
        return {
            "tag": self.tag,
            "keyword": self.keyword,
            "value_representation": self.VALUE_REPRESENTATION.value,
            "value_multiplicity": self.value_multiplicity,
            "value": self.value,
        }

    @requires_pandas
    def to_series(self):
        """
        Create a :class:`Series` representation of this instance.

        Returns
        -------
        pd.Series
            This instance as a :class:`Series`
        """
        import pandas as pd

        d = self.to_dict()
        return pd.Series(d)

    @property
    def value(self) -> Any:
        """
        Caches the parsed value or values of this instance.

        Returns
        -------
        Any
            This instance's parsed value or values
        """
        if self._value is None:
            self._value = self.parse_values()
        return self._value

    @property
    def is_private(self) -> bool:
        """
        Checks whether this data element is private or not.

        Returns
        -------
        bool
            Whether this data element is private or not
        """
        # TODO: This should probably be changed to simply check if the tag's
        # group number is odd.
        pattern = self.PRIVATE_ELEMENT_DESCRIPTION_PATTERN
        description = self.raw.description()
        return bool(re.match(pattern, description))

    @property
    def is_public(self) -> bool:
        """
        Checks whether this data element is public or not.

        Returns
        -------
        bool
            Whether this data element is public or not
        """
        return not self.is_private
