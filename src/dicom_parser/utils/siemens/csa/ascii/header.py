"""
Definition of the :class:`CsaAsciiHeader` class which handles the parsing of
`CSA header <https://nipy.org/nibabel/dicom/siemens_csa.html>`_ values
returned by `pydicom <https://github.com/pydicom/pydicom>`_ as bytes.
"""
import re
from typing import Union

from dicom_parser.utils.siemens.csa.ascii.element import CsaAsciiElement
from dicom_parser.utils.siemens.csa.ascii.parser import CsaAsciiParser


class CsaAsciiHeader:

    #: A pattern used to the extract the header information from the raw value.
    ASCCONV_HEADER_PATTERN = r"### ASCCONV BEGIN(.*?)### ASCCONV END ###"

    #: A pattern used to slice the entire header into single raw (string)
    #: values.
    ASCCONV_ELEMENT_PATTERN = r"([A-Z][^\n]*)"

    # The header's ASCII-based character encoding.
    ENCODING = "ISO-8859-1"

    def __init__(self, header: Union[str, bytes]):
        """
        Decodes the header and sets empty property caches to be overriden on
        request.

        Parameters
        ----------
        header : Union[str, bytes]
            Raw ASCCONV header information
        """
        self.raw = self.extract_ascii_header(header)

        # Property cache
        self._raw_elements = []
        self._parsed = {}
        self._elements = []

    @classmethod
    def extract_ascii_header(cls, raw_header: Union[str, bytes]) -> str:
        """
        Returns the decoded and extracted header information from the full
        data element's value.

        Returns
        -------
        str
            Decoded clean header information
        """
        if isinstance(raw_header, bytes):
            raw_header = raw_header.decode(cls.ENCODING)
        matches = re.findall(
            cls.ASCCONV_HEADER_PATTERN, raw_header, flags=re.DOTALL
        )
        return matches[0] if matches else ""

    def extract_elements(self) -> list:
        """
        Splits the decoded header information into a list of raw (string) data
        elements, each containing a key-value pair.
        The first item is skipped because it is an unrequired heading.

        Returns
        -------
        list
            CSA data elements in raw string format
        """
        elements = re.findall(self.ASCCONV_ELEMENT_PATTERN, self.raw)
        return elements[1:]

    def create_elements(self, raw_elements: list = None) -> list:
        """
        Creates
        :class:`~dicom_parser.utils.siemens.csa.ascii.element.CsaAsciiElement`
        instances that parse the key and the value.

        Parameters
        ----------
        raw_elements : list
            Raw ASCCONV CSA header elements

        Returns
        -------
        list
            :class:`~dicom_parser.utils.siemens.csa.ascii.element.CsaAsciiElement`
            instances.
        """
        raw_elements = raw_elements or self.raw_elements
        return [CsaAsciiElement(raw_element) for raw_element in raw_elements]

    def parse(self, elements: list = None) -> dict:
        """
        Parses a list of
        :class:`~dicom_parser.utils.siemens.csa.ascii.element.CsaAsciiElement`
        instances (or all if left None) as a dictionary.

        Parameters
        ----------
        elements : list, optional
            :class:`~dicom_parser.utils.siemens.csa.ascii.element.CsaAsciiElement`
            instances, by default None

        Returns
        -------
        dict
            Header information as a dictionary
        """
        elements = elements or self.elements
        parser = CsaAsciiParser()
        for element in elements:
            parser.parse(element)
        return parser.parsed

    @property
    def raw_elements(self) -> list:
        """
        Caches the raw (sting) CSA data elements as a private attribute.

        Returns
        -------
        list
            Raw CSA header data elements
        """
        if not self._raw_elements:
            self._raw_elements = self.extract_elements()
        return self._raw_elements

    @property
    def elements(self) -> list:
        """
        Caches the
        :class:`~dicom_parser.utils.siemens.csa.ascii.element.CsaAsciiElement`
        instances representing the entire header information.

        Returns
        -------
        list
            :class:`~dicom_parser.utils.siemens.csa.ascii.element.CsaAsciiElement`
            instances
        """
        if not self._elements:
            self._elements = self.create_elements()
        return self._elements

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
