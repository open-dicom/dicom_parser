"""
Definition of the :class:`~dicom_parser.utils.siemens.csa.header.CsaHeader`
class which handles the parsing of
`CSA header <https://nipy.org/nibabel/dicom/siemens_csa.html>`_ values
returned by `pydicom <https://github.com/pydicom/pydicom>`_ as bytes.

"""


import re

from dicom_parser.utils.siemens.csa.data_element import CsaDataElement
from dicom_parser.utils.siemens.csa.parser import CsaParser


class CsaHeader:
    """
    Represents a full CSA header data element, i.e. either
    (0029, 1010)/`"CSA Image Header Info"` or (0029, 1020)/`"CSA Series Header Info"`,
    and provides access to the header as a parsed dictionary.
    This implementation is heavily based on
    `dicom2nifti <https://github.com/icometrix/dicom2nifti>`_'s
    code (particularly
    `this module <https://github.com/icometrix/dicom2nifti/blob/6722420a7673d36437e4358ce3cb2a7c77c91820/dicom2nifti/convert_siemens.py#L342>`_).

    """

    # The header's ASCII-based character encoding.
    ENCODING = "ISO-8859-1"

    # A pattern used to the extract the header information from the raw element.
    CSA_HEADER_PATTERN = r"### ASCCONV BEGIN(.*?)### ASCCONV END ###"

    # A pattern used to slice the entire header into single raw (string) elements.
    ELEMENT_PATTERN = r"([A-Z][^\n]*)"

    def __init__(self, header: bytes):
        """
        Decodes the header and sets empty property caches to be overriden on request.

        Parameters
        ----------
        header : bytes
            Raw CSA header information as returned by pydicom
        """

        self.raw = header
        self.decoded = self.get_header_information()

        # Property cache
        self._raw_elements = []
        self._parsed = {}
        self._csa_data_elements = []

    def decode(self) -> str:
        """
        Decodes the raw (ASCII) information to string.

        Returns
        -------
        str
            Decoded information
        """

        return self.raw.decode(self.ENCODING)

    def get_header_information(self) -> str:
        """
        Returns the decoded and extracted header information from the full
        data element's value.

        Returns
        -------
        str
            Decoded clean header information
        """

        decoded = self.decode()
        matches = re.findall(self.CSA_HEADER_PATTERN, decoded, flags=re.DOTALL)
        return matches[0] if matches else ""

    def get_raw_data_elements(self) -> list:
        """
        Splits the decoded header information into a list of raw (string) data
        elements, each containing a key-value pair.
        The first item is skipped because it is an unrequired heading.

        Returns
        -------
        list
            CSA data elements in raw string format
        """

        return re.findall(self.ELEMENT_PATTERN, self.decoded)[1:]

    def create_csa_data_elements(self, raw_elements: list = None) -> list:
        """
        Creates :class:`~dicom_parser.utils.siemens.csa.data_element.CsaDataElement`
        instances that parse the key and the value

        Parameters
        ----------
        raw_elements : list
            Raw (string) CSA header elements

        Returns
        -------
        list
            :class:`~dicom_parser.utils.siemens.csa.data_element.CsaDataElement`
            instances.
        """

        raw_elements = raw_elements or self.raw_elements
        return [CsaDataElement(raw_element) for raw_element in raw_elements]

    def parse(self, csa_data_elements: list = None) -> dict:
        """
        Parses a list of
        :class:`~dicom_parser.utils.siemens.csa.data_element.CsaDataElement`
        instances (or all if left None) as a dictionary.

        Parameters
        ----------
        csa_data_elements : list, optional
            :class:`~dicom_parser.utils.siemens.csa.data_element.CsaDataElement`
            instances, by default None

        Returns
        -------
        dict
            Header information as a dictionary
        """

        csa_data_elements = csa_data_elements or self.csa_data_elements
        parser = CsaParser()
        for element in csa_data_elements:
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
            self._raw_elements = self.get_raw_data_elements()
        return self._raw_elements

    @property
    def csa_data_elements(self) -> list:
        """
        Caches the :class:`~dicom_parser.utils.siemens.csa.data_element.CsaDataElement`
        instances representing the entire header information.

        Returns
        -------
        list
            :class:`~dicom_parser.utils.siemens.csa.data_element.CsaDataElement` instances
        """

        if not self._csa_data_elements:
            self._csa_data_elements = self.create_csa_data_elements()
        return self._csa_data_elements

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
            Number of slices encoded as a 2D mosaic.
        """

        return self.parsed["SliceArray"]["Size"]
