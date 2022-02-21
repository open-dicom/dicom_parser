from unittest import TestCase

import pydicom
from dicom_parser.utils.siemens.csa.ascii.ascconv import (
    parse_ascconv,
    parse_ascconv_text,
)
from dicom_parser.utils.siemens.private_tags import SIEMENS_PRIVATE_TAGS
from tests.fixtures import TEST_RSFMRI_IMAGE_PATH
from tests.utils.siemens.csa.ascii.fixtures import (
    PARSED_ELEMENTS,
    RAW_ELEMENTS,
)


class CsaParsingTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        dcm = pydicom.dcmread(TEST_RSFMRI_IMAGE_PATH)
        tag = SIEMENS_PRIVATE_TAGS["CSASeriesHeaderInfo"]
        cls.series_header_info = dcm.get(tag).value
        cls.csa_data, cls.first_line_info = parse_ascconv(
            cls.series_header_info.decode("ISO-8859-1"), delimiter='""'
        )

    def test_key_and_value_ordered(self):
        first_key = "ulVersion"
        first_value = 51130001
        found_keys = list(self.csa_data)
        self.assertEqual(found_keys[0], first_key)
        self.assertEqual(self.csa_data[found_keys[0]], first_value)

    def test_nested_value(self):
        self.assertEqual(
            self.csa_data["sGRADSPEC"]["asGPAData"][0]["sEddyCompensationY"][
                "aflTimeConstant"
            ][1],
            0.917683601379,
        )

    def test_parse_fragment(self):
        out = parse_ascconv_text(RAW_ELEMENTS)
        self.assertEqual(out, PARSED_ELEMENTS)
