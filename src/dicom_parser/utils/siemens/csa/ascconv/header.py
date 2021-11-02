"""
Definition of the :class:`~dicom_parser.utils.siemens.csa.header.CsaHeader`
class which handles the parsing of
`CSA header <https://nipy.org/nibabel/dicom/siemens_csa.html>`_ values
returned by `pydicom <https://github.com/pydicom/pydicom>`_ as bytes.
"""
import re

from dicom_parser.utils.siemens.csa.ascconv.ascconv_element import (
    AscconvElement,
)
from dicom_parser.utils.siemens.csa.ascconv.ascconv_parser import AscconvParser


class AscconvHeader:

    #: A pattern used to the extract the header information from the raw value.
    ASCCONV_HEADER_PATTERN = r"### ASCCONV BEGIN(.*?)### ASCCONV END ###"

    #: A pattern used to slice the entire header into single raw (string)
    #: values.
    ASCCONV_ELEMENT_PATTERN = r"([A-Z][^\n]*)"

    #: The header's ASCII-based character encoding.
    ENCODING = "ISO-8859-1"

    def __init__(self, header: str):
        """
        Decodes the header and sets empty property caches to be overriden on
        request.

        Parameters
        ----------
        header : bytes
            Raw ASCCONV header information
        """
        self.raw = header
        self.decoded = self.decode()
        if self.csa_type == 2:
            # Omit CSA header 2 prefix ('SV10')
            self.unpacker.pointer = 4
        self.decoded_ascconv = self.get_ascconv_header()

        # Property cache
        self._raw_ascconv_elements = []
        self._parsed = {}
        self._ascconv_elements = []

    def decode(self) -> str:
        """
        Decodes the raw (ASCII) information to string.

        Returns
        -------
        str
            Decoded information
        """
        return self.raw.decode(self.ENCODING)

    def get_ascconv_header(self) -> str:
        """
        Returns the decoded and extracted header information from the full
        data element's value.

        Returns
        -------
        str
            Decoded clean header information
        """
        matches = re.findall(
            self.ASCCONV_HEADER_PATTERN, self.decoded_ascconv, flags=re.DOTALL
        )
        return matches[0] if matches else ""

    def get_raw_ascconv_elements(self) -> list:
        """
        Splits the decoded header information into a list of raw (string) data
        elements, each containing a key-value pair.
        The first item is skipped because it is an unrequired heading.

        Returns
        -------
        list
            CSA data elements in raw string format
        """
        elements = re.findall(
            self.ASCCONV_ELEMENT_PATTERN, self.decoded_ascconv
        )
        return elements[1:]

    def create_ascconv_elements(self, raw_elements: list = None) -> list:
        """
        Creates
        :class:`~dicom_parser.utils.siemens.csa.ascconv_element.AscconvElement`
        instances that parse the key and the value.

        Parameters
        ----------
        raw_elements : list
            Raw ASCCONV CSA header elements

        Returns
        -------
        list
            :class:`~dicom_parser.utils.siemens.csa.ascconv_element.AscconvElement`
            instances.
        """
        raw_elements = raw_elements or self.raw_ascconv_elements
        return [AscconvElement(raw_element) for raw_element in raw_elements]

    def parse(self, ascconv_elements: list = None) -> dict:
        """
        Parses a list of
        :class:`~dicom_parser.utils.siemens.csa.ascconv_element.AscconvElement`
        instances (or all if left None) as a dictionary.

        Parameters
        ----------
        ascconv_elements : list, optional
            :class:`~dicom_parser.utils.siemens.csa.ascconv_element.AscconvElement`
            instances, by default None

        Returns
        -------
        dict
            Header information as a dictionary
        """
        ascconv_elements = ascconv_elements or self.ascconv_elements
        parser = AscconvParser()
        for element in ascconv_elements:
            parser.parse(element)
        return parser.parsed

    @property
    def raw_ascconv_elements(self) -> list:
        """
        Caches the raw (sting) CSA data elements as a private attribute.

        Returns
        -------
        list
            Raw CSA header data elements
        """
        if not self._raw_ascconv_elements:
            self._raw_ascconv_elements = self.get_raw_ascconv_elements()
        return self._raw_ascconv_elements

    @property
    def ascconv_elements(self) -> list:
        """
        Caches the
        :class:`~dicom_parser.utils.siemens.csa.ascconv_element.AscconvElement`
        instances representing the entire header information.

        Returns
        -------
        list
            :class:`~dicom_parser.utils.siemens.csa.ascconv_element.AscconvElement`
            instances
        """
        if not self._ascconv_elements:
            self._ascconv_elements = self.create_ascconv_elements()
        return self._ascconv_elements

    @property
    def parsed(self) -> dict:
        """
        Caches the parsed dictionary as a private attribute.

        Returns
        -------
        dict
            Header information as dictionary
        """
        if not self._parsed:
            self._parsed = self.parse()
        return self._parsed

    @property
    def n_slices(self) -> int:
        """
        Returns the number of slices (tiles) in a mosaic.

        Returns
        -------
        int
            Number of slices encoded as a 2D mosaic
        """
        return self.parsed["SliceArray"]["Size"]
