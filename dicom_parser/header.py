"""
Definition of the Header class, which extends the functionality of
`pydicom <https://github.com/pydicom/pydicom>`_.

"""

from dicom_parser.parser import Parser
from dicom_parser.utils.private_tags import PRIVATE_TAGS
from dicom_parser.utils.read_file import read_file
from dicom_parser.utils.sequence_detector.sequence_detector import SequenceDetector
from pydicom.dataelem import DataElement


class Header:
    """
    Facilitates access to DICOM_ header information from pydicom_'s FileDataset_.

    .. _DICOM: https://www.dicomstandard.org/
    .. _pydicom: https://github.com/pydicom/pydicom
    .. _FileDataset: https://github.com/pydicom/pydicom/blob/master/pydicom/dataset.py

    """

    sequence_identifiers = {"mr": ["ScanningSequence", "SequenceVariant"]}

    def __init__(self, raw, parser=Parser, sequence_detector=SequenceDetector):
        """
        Header is meant to be initialized with a pydicom_ FileDataset_
        representing a single image's header, or a string representing
        the path to a dicom image file, or a :class:`~pathlib.Path` instance.

        Parameters
        ----------
        raw : pydicom.dataset.FileDataset / path string or pathlib.Path instance
            DICOM_ image header information or path.
        parser : type
            An object with a public `parse()` method that may be used to parse
            data elements, by default Parser.

        .. _pydicom: https://github.com/pydicom/pydicom
        .. _FileDataset: https://github.com/pydicom/pydicom/blob/master/pydicom/dataset.py
        .. _DICOM: https://www.dicomstandard.org/

        """

        self.parser = parser()
        self.sequence_detector = sequence_detector()
        self.raw = read_file(raw)
        self.manufacturer = self.get("Manufacturer")
        self.detected_sequence = self.detect_sequence()

    def __getitem__(self, key):
        """
        Provide dictionary like indexing-operator functionality.

        Parameters
        ----------
        key : str or tuple or list
            The key or list of keys for which to retrieve header information

        Returns
        -------
        [type]
            Parsed header information of the given key or keys
        """

        return self.get(key, missing_ok=False)

    def detect_sequence(self) -> str:
        """
        Returns the detected imaging sequence using the modality's sequence
        identifying header information.

        Returns
        -------
        str
            Imaging sequence name
        """

        modality = self.get("Modality").lower()
        sequence_identifiers = self.sequence_identifiers.get(modality)
        sequece_identifying_values = self.get(sequence_identifiers)
        return self.sequence_detector.detect(modality, sequece_identifying_values)

    def get_element_by_keyword(self, keyword: str) -> DataElement:
        """
        Returns a pydicom_ DataElement_ from the header (FileDataset_ isntance)
        by keyword.

        .. _pydicom: https://github.com/pydicom/pydicom
        .. _DataElement: https://github.com/pydicom/pydicom/blob/master/pydicom/dataelem.py
        .. _FileDataset: https://github.com/pydicom/pydicom/blob/master/pydicom/dataset.py

        Parameters
        ----------
        keyword : str
            The keyword representing the DICOM data element in pydicom

        Returns
        -------
        DataElement
            The requested data element
        """

        value = self.raw.data_element(keyword)
        if isinstance(value, DataElement):
            return value
        raise KeyError(f"The keyword: '{keyword}' does not exist in the header!")

    def get_element_by_tag(self, tag: tuple) -> DataElement:
        """
        Returns a pydicom_ DataElement_ from the header (FileDataset_ isntance)
        by tag.

        .. _pydicom: https://github.com/pydicom/pydicom
        .. _DataElement: https://github.com/pydicom/pydicom/blob/master/pydicom/dataelem.py
        .. _FileDataset: https://github.com/pydicom/pydicom/blob/master/pydicom/dataset.py

        Parameters
        ----------
        tag : tuple
            The DICOM tag of the desired data element

        Returns
        -------
        DataElement
            The requested data element
        """

        value = self.raw.get(tag)
        if isinstance(value, DataElement):
            return value
        raise KeyError(f"The tag: {tag} does not exist in the header!")

    def get_element(self, tag_or_keyword) -> DataElement:
        """
        Returns a pydicom_ DataElement_ from the associated FileDataset_ either by
        tag (passed as a tuple) or a keyword (passed as a string). If none found
        or the tag or keyword are invalid, returns None.

        .. _pydicom: https://github.com/pydicom/pydicom
        .. _DataElement: https://github.com/pydicom/pydicom/blob/master/pydicom/dataelem.py
        .. _FileDataset: https://github.com/pydicom/pydicom/blob/master/pydicom/dataset.py

        Parameters
        ----------
        tag_or_keyword : tuple or str
            Tag or keyword representing the requested data element

        Returns
        -------
        DataElement
            The requested data element
        """

        # By keyword
        if type(tag_or_keyword) is str:
            return self.get_element_by_keyword(tag_or_keyword)

        # By tag
        elif type(tag_or_keyword) is tuple:
            return self.get_element_by_tag(tag_or_keyword)

        # If not a keyword or a tag, raise a TypeError
        else:
            raise TypeError(
                f"Invalid data element identifier: {tag_or_keyword} of type {type(tag_or_keyword)}!\nData elements may only be queried using a string represeting a keyword or a tuple of two strings representing a tag!"  # noqa
            )

    def get_raw_value(self, tag_or_keyword):
        """
        Returns the raw value for the requested data element, as returned by
        pydicom_. If none is found will return None.

        .. _pydicom: https://github.com/pydicom/pydicom

        Parameters
        ----------
        tag_or_keyword : tuple or str
            Tag or keyword representing the requested data element.

        Returns
        -------
        type
            The raw value of the data element
        """

        element = self.get_element(tag_or_keyword)
        return element.value

    def get_parsed_value(self, tag_or_keyword):
        """
        Returns the parsed value of pydicom_ data element using the this class's
        parser attribute. The data element may be represented by tag or by its
        pydicom_ keyword. If none is found will return None.

        .. _pydicom: https://github.com/pydicom/pydicom

        Parameters
        ----------
        tag_or_keyword : tuple or str
            Tag or keyword representing the requested data element

        Returns
        -------
        type
            Parsed data element value
        """

        element = self.get_element(tag_or_keyword)
        return self.parser.parse(element)

    def get_private_tag(self, keyword: str) -> tuple:
        """
        Returns a vendor-specific private tag corresponding to the provided keyword,
        if the tag is registered (see the :mod:`~dicom_parser.utils.private_tags` module).
        This is required because pydicom does not offer keyword access to private tags.

        Parameters
        ----------
        keyword : str
            Private data element keyword

        Returns
        -------
        tuple
            Private data element tag
        """

        if keyword != "Manufacturer":
            manufacturer_private_tags = PRIVATE_TAGS.get(self.manufacturer, {})
            return manufacturer_private_tags.get(keyword)

    def get(
        self, tag_or_keyword, default=None, parsed: bool = True, missing_ok: bool = True
    ):
        """
        Returns the value of a pydicom data element, selected by tag (`tuple`) or
        keyword (`str`). Input may also be a `list` of such identifiers, in which
        case a dictionary will be returned with the identifiers as keys and header
        information as values.

        Parameters
        ----------
        tag_or_keyword : tuple or str, or list
            Tag or keyword representing the requested data element, or a list of such.
        parsed : bool, optional
            Whether to return a parsed or raw value (the default is True, which will
            return the parsed value).

        Returns
        -------
        type
            The requested data element value (or a dict for multiple values)
        """

        get_method = self.get_parsed_value if parsed else self.get_raw_value
        value = None
        if isinstance(tag_or_keyword, str):
            tag_or_keyword = self.get_private_tag(tag_or_keyword) or tag_or_keyword
        try:
            if isinstance(tag_or_keyword, (str, tuple)):
                value = get_method(tag_or_keyword)
            elif isinstance(tag_or_keyword, list):
                value = {item: get_method(item) for item in tag_or_keyword}
        except (KeyError, TypeError):
            if not missing_ok:
                raise
        return value or default
