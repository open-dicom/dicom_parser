"""
Definition of the Header class, which extends the functionality of
`pydicom <https://github.com/pydicom/pydicom>`_.

"""
import json
import pandas as pd

from collections.abc import KeysView
from dicom_parser.data_element import DataElement
from dicom_parser.utils.format_header_df import format_header_df
from dicom_parser.utils.private_tags import PRIVATE_TAGS
from dicom_parser.utils.read_file import read_file
from dicom_parser.utils.sequence_detector.sequence_detector import SequenceDetector
from dicom_parser.utils.value_representation import ValueRepresentation
from dicom_parser.utils.vr_to_data_element import get_data_element_class
from pydicom.dataelem import DataElement as PydicomDataElement
from types import GeneratorType


class Header:
    """
    Facilitates access to DICOM_ header information from pydicom_'s FileDataset_.

    .. _DICOM: https://www.dicomstandard.org/
    .. _pydicom: https://github.com/pydicom/pydicom
    .. _FileDataset: https://github.com/pydicom/pydicom/blob/master/pydicom/dataset.py

    """

    sequence_identifiers = {
        "Magnetic Resonance": ["ScanningSequence", "SequenceVariant"]
    }
    DATAFRAME_COLUMNS = "Tag", "Keyword", "VR", "VM", "Value"
    DATAFRAME_INDEX = "Tag"

    def __init__(self, raw, sequence_detector=SequenceDetector):
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

        self.sequence_detector = sequence_detector()
        self.raw = read_file(raw, read_data=False)
        self.manufacturer = self.get("Manufacturer")
        self.detected_sequence = self.detect_sequence()
        self._as_dict = None

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

    def __str__(self) -> str:
        base = self.to_dataframe(exclude=ValueRepresentation.SQ, private=False)
        sequences = self.get_data_elements(value_representation=ValueRepresentation.SQ)
        privates = self.to_dataframe(private=True)
        sequences_string = ""
        if sequences:
            sequences_string = "\n\nSequences\n=========\n"
            separator = "_" * 100 + "\n\n"
            sequences_string += separator.join(
                [str(sequence) for sequence in sequences]
            )
        privates_string = "\n\nPrivate Data Elements\n=====================\n"
        privates_string = (
            privates_string + format_header_df(privates) if not privates.empty else ""
        )
        return format_header_df(base) + sequences_string + privates_string

    def __repr__(self) -> str:
        return self.__str__()

    def detect_sequence(self) -> str:
        """
        Returns the detected imaging sequence using the modality's sequence
        identifying header information.

        Returns
        -------
        str
            Imaging sequence name
        """

        modality = self.get("Modality")
        sequence_identifiers = self.sequence_identifiers.get(modality)
        sequence_identifying_values = self.get(sequence_identifiers)
        try:
            return self.sequence_detector.detect(modality, sequence_identifying_values)
        except NotImplementedError:
            pass

    def get_raw_element_by_keyword(self, keyword: str) -> PydicomDataElement:
        """
        Returns a pydicom_ PydicomDataElement_ from the header (FileDataset_ isntance)
        by keyword.

        .. _pydicom: https://github.com/pydicom/pydicom
        .. _PydicomDataElement: https://github.com/pydicom/pydicom/blob/master/pydicom/dataelem.py
        .. _FileDataset: https://github.com/pydicom/pydicom/blob/master/pydicom/dataset.py

        Parameters
        ----------
        keyword : str
            The keyword representing the DICOM data element in pydicom

        Returns
        -------
        PydicomDataElement
            The requested data element
        """

        value = self.raw.data_element(keyword)
        if isinstance(value, PydicomDataElement):
            return value
        raise KeyError(f"The keyword: '{keyword}' does not exist in the header!")

    def get_raw_element_by_tag(self, tag: tuple) -> PydicomDataElement:
        """
        Returns a pydicom_ PydicomDataElement_ from the header (FileDataset_ isntance)
        by tag.

        .. _pydicom: https://github.com/pydicom/pydicom
        .. _PydicomDataElement: https://github.com/pydicom/pydicom/blob/master/pydicom/dataelem.py
        .. _FileDataset: https://github.com/pydicom/pydicom/blob/master/pydicom/dataset.py

        Parameters
        ----------
        tag : tuple
            The DICOM tag of the desired data element

        Returns
        -------
        PydicomDataElement
            The requested data element
        """

        value = self.raw.get(tag)
        if isinstance(value, PydicomDataElement):
            return value
        raise KeyError(f"The tag: {tag} does not exist in the header!")

    def get_raw_element(self, tag_or_keyword) -> PydicomDataElement:
        """
        Returns a pydicom_ PydicomDataElement_ from the associated FileDataset_ either by
        tag (passed as a tuple) or a keyword (passed as a string). If none found
        or the tag or keyword are invalid, returns None.

        .. _pydicom: https://github.com/pydicom/pydicom
        .. _PydicomDataElement: https://github.com/pydicom/pydicom/blob/master/pydicom/dataelem.py
        .. _FileDataset: https://github.com/pydicom/pydicom/blob/master/pydicom/dataset.py

        Parameters
        ----------
        tag_or_keyword : tuple or str
            Tag or keyword representing the requested data element

        Returns
        -------
        PydicomDataElement
            The requested data element
        """

        # By keyword
        if type(tag_or_keyword) is str:
            return self.get_raw_element_by_keyword(tag_or_keyword)
        # By tag
        elif type(tag_or_keyword) is tuple:
            return self.get_raw_element_by_tag(tag_or_keyword)

        # If not a keyword or a tag, raise a TypeError
        else:
            raise TypeError(
                f"Invalid data element identifier: {tag_or_keyword} of type {type(tag_or_keyword)}!\nData elements may only be queried using a string represeting a keyword or a tuple of two strings representing a tag!"  # noqa
            )

    def get_data_element(self, tag_or_keyword) -> DataElement:
        if isinstance(tag_or_keyword, (tuple, str)):
            raw_element = self.get_raw_element(tag_or_keyword)
        elif not isinstance(tag_or_keyword, PydicomDataElement):
            raise TypeError("Bad data element identifier!")
        else:
            raw_element = tag_or_keyword
        DataElementClass = get_data_element_class(raw_element.VR)
        data_element = DataElementClass(raw_element)
        if data_element.VALUE_REPRESENTATION == ValueRepresentation.SQ:
            data_element._value = [
                Header(raw_header) for raw_header in raw_element.value
            ]
        return data_element

    def get_data_elements(
        self, value_representation=None, exclude=None, private: bool = None
    ) -> list:
        data_elements = []
        filter_by_vr = isinstance(
            value_representation, (ValueRepresentation, list, tuple)
        )
        exclusions = isinstance(exclude, (ValueRepresentation, list, tuple))
        for data_element in self.data_elements:
            if isinstance(value_representation, ValueRepresentation):
                matching_vr = data_element.VALUE_REPRESENTATION == value_representation
            elif isinstance(value_representation, (list, tuple)):
                matching_vr = data_element.VALUE_REPRESENTATION in value_representation
            filtered = filter_by_vr and not matching_vr
            if isinstance(exclude, ValueRepresentation):
                excluded_vr = data_element.VALUE_REPRESENTATION == exclude
            elif isinstance(exclude, (list, tuple)):
                excluded_vr = data_element.VALUE_REPRESENTATION in exclude
            excluded = exclusions and excluded_vr
            private_filter = False
            if private is not None:
                private_filter = data_element.is_private != private
            if not (filtered or excluded or private_filter):
                data_elements.append(data_element)
        return data_elements

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

        element = self.get_raw_element(tag_or_keyword)
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

        data_element = self.get_data_element(tag_or_keyword)
        return data_element.value

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
        self,
        tag_or_keyword,
        default=None,
        parsed: bool = True,
        missing_ok: bool = True,
        as_json: bool = False,
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

        # Assignes the required method based on the `parsed` parameter's value
        get_method = self.get_parsed_value if parsed else self.get_raw_value

        # Tries to find a private tags tuple if the given tag_or_keyword is a
        # keyword that has been registered in the private_tags module
        if isinstance(tag_or_keyword, str):
            tag_or_keyword = self.get_private_tag(tag_or_keyword) or tag_or_keyword

        # Get the requested value
        value = None
        try:
            if isinstance(tag_or_keyword, (str, tuple)):
                value = get_method(tag_or_keyword)
            elif isinstance(tag_or_keyword, list):
                value = {item: get_method(item) for item in tag_or_keyword}
        except (KeyError, TypeError):
            if not missing_ok:
                raise
        if value and as_json:
            value = json.dumps(value, indent=4, sort_keys=True, default=str)
        return value or default

    def to_dict(self, parsed: bool = True) -> dict:
        return {
            data_element.keyword: self.get(data_element.keyword, parsed=parsed)
            for data_element in self.data_elements
        }

    def to_dataframe(
        self,
        data_elements: list = None,
        value_representation=None,
        exclude=None,
        private: bool = None,
    ) -> pd.DataFrame:
        data_elements = [
            data_element.to_series()
            for data_element in data_elements
            or self.get_data_elements(
                value_representation=value_representation,
                exclude=exclude,
                private=private,
            )
        ]
        df = pd.concat(data_elements, axis=1).transpose()
        df.columns = self.DATAFRAME_COLUMNS
        df.set_index(self.DATAFRAME_INDEX, inplace=True)
        df.style.set_properties(**{"text-align": "left"})
        return df

    @property
    def data_elements(self) -> GeneratorType:
        for element in self.raw:
            if element.tag != ("7fe0", "0010"):
                yield self.get_data_element(element)

    @property
    def as_dict(self) -> dict:
        if not isinstance(self._as_dict, dict):
            self._as_dict = self.to_dict()
        return self._as_dict

    @property
    def keys(self) -> KeysView:
        return self.as_dict.keys()
