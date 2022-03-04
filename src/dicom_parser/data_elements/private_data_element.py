"""
Definition of the :class:`PrivateDataElement` class, representing a single "UN"
data element.
"""
from types import FunctionType
from typing import Any

from dicom_parser.data_element import DataElement
from dicom_parser.utils.siemens.private_tags import (
    parse_siemens_b_matrix,
    parse_siemens_bandwith_per_pixel_phase_encode,
    parse_siemens_csa_header,
    parse_siemens_gradient_direction,
    parse_siemens_number_of_slices_in_mosaic,
    parse_siemens_slice_timing,
)
from dicom_parser.utils.value_representation import ValueRepresentation
from pydicom.dataelem import DataElement as PydicomDataElement

#: A dictionary matching private data elements to their appropriate parsing
#: method.
TAG_TO_PARSER = {
    ("0019", "100a"): parse_siemens_number_of_slices_in_mosaic,
    ("0019", "100b"): float,
    ("0019", "100c"): int,
    ("0019", "100e"): parse_siemens_gradient_direction,
    ("0019", "1027"): parse_siemens_b_matrix,
    ("0019", "1028"): parse_siemens_bandwith_per_pixel_phase_encode,
    ("0019", "1029"): parse_siemens_slice_timing,
    ("0029", "1010"): parse_siemens_csa_header,
    ("0029", "1020"): parse_siemens_csa_header,
}


class PrivateDataElement(DataElement):
    #: The VR value of data elements represented by this class.
    VALUE_REPRESENTATION = ValueRepresentation.UN

    def __init__(self, raw: PydicomDataElement):
        """
        Intialize a new instance of  this class.

        Parameters
        ----------
        raw : PydicomDataElement
            pydicom's representation of this data element
        """
        super().__init__(raw)

    def parse_value(self, value: bytes) -> Any:
        """
        Tries to parse private data element values using a custom function or
        by simply calling :func:`bytes.decode`.

        Parameters
        ----------
        value : bytes
            Raw private data element value

        Returns
        -------
        Any
            Parsed private data element value
        """
        # Try to call a custom parser function.
        method: FunctionType = TAG_TO_PARSER.get(self.tag)
        if method:
            return method(value)

        # Try to decode.
        elif isinstance(value, bytes):
            try:
                return value.decode().strip()
            except UnicodeDecodeError:
                pass

        # Otherwise, simply return the raw value.
        return value
