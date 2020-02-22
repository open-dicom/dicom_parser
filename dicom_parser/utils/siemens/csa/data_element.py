"""
Definition of a single CSA header data element. These elements are parsed from
the full string header using new line characters.

"""

import re


class CsaDataElement:
    """
    Represents a single CSA header data element as extracted from the raw
    header information.

    """

    # The element's key parts are often prefixed with lowercase characters that
    # may be removed.
    CLEAN_PART_PATTERN = r"[A-Z].*"

    # Parts containing a `[<digit>]` pattern indicate a list.
    LIST_PART_PATTERN = r"\[\d+\]"

    def __init__(self, raw_element: str):
        """
        Initialized with a raw (string) data element as extracted from the header
        information.

        Parameters
        ----------
        raw_element : str
            CSA header data element as string
        """

        self.raw_element = raw_element
        self.key, self.value = self.split()

    def clean_part(self, part: str) -> str:
        """
        Returns a the part's name without any prefixed lowercase characters.

        Parameters
        ----------
        part : str
            One of the listed key's parts

        Returns
        -------
        str
            Prefix-omitted part name
        """

        key_pattern = re.search(self.CLEAN_PART_PATTERN, part)
        return key_pattern.group() if key_pattern else part

    def key_to_list(self, chained_key: str) -> list:
        """
        The string data elements represents nested keys using a '.' character.
        Returns a clean (prefix-omitted) list of the nested key structure.

        Parameters
        ----------
        chained_key : str
            CSA header data element key

        Returns
        -------
        list
            Clean and listed representation of the provided key
        """

        return [self.clean_part(part) for part in chained_key.split(".")]

    def split(self) -> tuple:
        """
        Splits the raw CSA element to a clean and listed key and a value.

        Returns
        -------
        tuple
            key, value
        """

        tab_split = self.raw_element.split("\t")
        key = self.key_to_list(tab_split[0])
        return key, tab_split[-1]

    def search_array_pattern(self, part: str) -> int:
        """
        Checks if the pattern indicating a particular key part represents an array.

        Parameters
        ----------
        part : str
            Some part of a listed key

        Returns
        -------
        int
            The value's index if array pattern found, else None
        """

        match = re.search(self.LIST_PART_PATTERN, part)
        return int(match.group()[1:-1]) if match else None
