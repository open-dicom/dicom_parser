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
from types import FunctionType

TAG_TO_DEFINITION = {
    ("0019", "100a"): {"method": parse_siemens_number_of_slices_in_mosaic},
    ("0019", "100b"): {"method": float},
    ("0019", "100c"): {"method": int},
    ("0019", "100e"): {"method": parse_siemens_gradient_direction},
    ("0019", "1027"): {"method": parse_siemens_b_matrix},
    ("0019", "1028"): {"method": parse_siemens_bandwith_per_pixel_phase_encode},
    ("0019", "1029"): {"method": parse_siemens_slice_timing},
    ("0029", "1010"): {"method": parse_siemens_csa_header},
    ("0029", "1020"): {"method": parse_siemens_csa_header},
}


class PrivateDataElement(DataElement):
    VALUE_REPRESENTATION = ValueRepresentation.UN

    def __init__(self, raw: PydicomDataElement):
        super().__init__(raw)
        self.definition = TAG_TO_DEFINITION.get(self.tag, {})
        self.update_from_definition()

    def update_from_definition(self) -> None:
        self.value_representation = self.definition.get(
            "value_representation", self.VALUE_REPRESENTATION
        )

    def parse_value(self, value: bytes):
        method: FunctionType = self.definition.get("method")
        if method:
            return method(self.raw.value)
        return self.raw.value
