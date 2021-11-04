from unittest import TestCase

import pydicom
from dicom_parser.utils.siemens.csa.ascconv import AscconvHeader
from dicom_parser.utils.siemens.csa.ascconv.data_element import AscconvElement
from dicom_parser.utils.siemens.private_tags import SIEMENS_PRIVATE_TAGS
from tests.fixtures import TEST_RSFMRI_IMAGE_PATH


class AscconvHeaderTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        dcm = pydicom.dcmread(TEST_RSFMRI_IMAGE_PATH)
        tag = SIEMENS_PRIVATE_TAGS["CSASeriesHeaderInfo"]
        cls.series_header_info = dcm.get(tag).value
        cls.ascconv_header = AscconvHeader(cls.series_header_info)

    def test_init_stores_raw(self):
        self.assertEqual(self.ascconv_header.raw, self.series_header_info)

    def test_init_decodes_raw_info(self):
        self.assertIsInstance(self.ascconv_header.decoded, str)

    def test_init_prepares_cached_variables(self):
        fresh_header = AscconvHeader(self.series_header_info)
        self.assertEqual(fresh_header._raw_elements, [])
        self.assertEqual(fresh_header._parsed, {})
        self.assertEqual(fresh_header._ascconv_data_elements, [])

    def test_decode(self):
        decoded = self.ascconv_header.decode()
        self.assertIsInstance(decoded, str)

    def test_get_header_information(self):
        header_information = self.ascconv_header.get_header_information()
        self.assertIsInstance(header_information, str)
        self.assertEqual(len(header_information), 140843)

    def test_get_raw_data_elements(self):
        raw_elements = self.ascconv_header.get_raw_data_elements()
        self.assertIsInstance(raw_elements, list)
        self.assertEqual(len(raw_elements), 2466)

    def test_create_ascconv_data_elements(self):
        ascconv_elements = self.ascconv_header.create_ascconv_data_elements()
        self.assertIsInstance(ascconv_elements, list)
        self.assertEqual(len(ascconv_elements), 2466)
        self.assertIsInstance(ascconv_elements[0], AscconvElement)

    def test_parse_returns_dict(self):
        parsed = self.ascconv_header.parse()
        self.assertIsInstance(parsed, dict)

    def test_parse_results_for_nested_dict_value(self):
        parsed = self.ascconv_header.parse()
        slice_array_size = 64
        value = parsed["SliceArray"]["Size"]
        self.assertEqual(slice_array_size, value)
        k_space_slice_resolution = 1
        value = parsed["KSpace"]["SliceResolution"]
        self.assertEqual(k_space_slice_resolution, value)

    def test_parse_results_for_nested_list_value(self):
        parsed = self.ascconv_header.parse()
        value = parsed["CoilSelectMeas"]["RxCoilSelectData"]
        self.assertIsInstance(value, list)
        self.assertEqual(len(value), 2)

    def test_raw_elements_property(self):
        self.assertIsInstance(self.ascconv_header.raw_elements, list)
        self.assertIs(
            self.ascconv_header.raw_elements, self.ascconv_header.raw_elements
        )

    def test_ascconv_data_elements_property(self):
        self.assertIsInstance(self.ascconv_header.ascconv_data_elements, list)
        self.assertIs(
            self.ascconv_header.ascconv_data_elements,
            self.ascconv_header.ascconv_data_elements,
        )

    def test_parsed_property(self):
        self.assertIsInstance(self.ascconv_header.parsed, dict)
        self.assertIs(self.ascconv_header.parsed, self.ascconv_header.parsed)

    def test_n_slices_property(self):
        result = self.ascconv_header.n_slices
        expected = self.ascconv_header.parsed["SliceArray"]["Size"]
        self.assertEqual(result, expected)
