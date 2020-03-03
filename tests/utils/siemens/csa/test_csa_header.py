import pydicom

from dicom_parser.utils.siemens.csa.data_element import CsaDataElement
from dicom_parser.utils.siemens.csa.header import CsaHeader
from dicom_parser.utils.siemens.private_tags import SIEMENS_PRIVATE_TAGS
from tests.fixtures import TEST_RSFMRI_IMAGE_PATH
from unittest import TestCase


class CsaHeaderTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        dcm = pydicom.dcmread(TEST_RSFMRI_IMAGE_PATH)
        tag = SIEMENS_PRIVATE_TAGS["CSASeriesHeaderInfo"]
        cls.series_header_info = dcm.get(tag).value
        cls.csa_header = CsaHeader(cls.series_header_info)

    def test_init_stores_raw(self):
        self.assertEqual(self.csa_header.raw, self.series_header_info)

    def test_init_decodes_raw_info(self):
        self.assertIsInstance(self.csa_header.decoded, str)

    def test_init_prepares_cached_variables(self):
        fresh_header = CsaHeader(self.series_header_info)
        self.assertEqual(fresh_header._raw_elements, [])
        self.assertEqual(fresh_header._parsed, {})
        self.assertEqual(fresh_header._csa_data_elements, [])

    def test_decode(self):
        decoded = self.csa_header.decode()
        self.assertIsInstance(decoded, str)

    def test_get_header_information(self):
        header_information = self.csa_header.get_header_information()
        self.assertIsInstance(header_information, str)
        self.assertEqual(len(header_information), 140843)

    def test_get_raw_data_elements(self):
        raw_elements = self.csa_header.get_raw_data_elements()
        self.assertIsInstance(raw_elements, list)
        self.assertEqual(len(raw_elements), 2466)

    def test_create_csa_data_elements(self):
        csa_elements = self.csa_header.create_csa_data_elements()
        self.assertIsInstance(csa_elements, list)
        self.assertEqual(len(csa_elements), 2466)
        self.assertIsInstance(csa_elements[0], CsaDataElement)

    def test_parse_returns_dict(self):
        parsed = self.csa_header.parse()
        self.assertIsInstance(parsed, dict)

    def test_parse_results_for_nested_dict_value(self):
        parsed = self.csa_header.parse()
        slice_array_size = 64
        value = parsed["SliceArray"]["Size"]
        self.assertEqual(slice_array_size, value)
        k_space_slice_resolution = 1
        value = parsed["KSpace"]["SliceResolution"]
        self.assertEqual(k_space_slice_resolution, value)

    def test_parse_results_for_nested_list_value(self):
        parsed = self.csa_header.parse()
        value = parsed["CoilSelectMeas"]["RxCoilSelectData"]
        self.assertIsInstance(value, list)
        self.assertEqual(len(value), 2)

    def test_raw_elements_property(self):
        self.assertIsInstance(self.csa_header.raw_elements, list)
        self.assertIs(self.csa_header.raw_elements, self.csa_header.raw_elements)

    def test_csa_data_elements_property(self):
        self.assertIsInstance(self.csa_header.csa_data_elements, list)
        self.assertIs(
            self.csa_header.csa_data_elements, self.csa_header.csa_data_elements
        )

    def test_parsed_property(self):
        self.assertIsInstance(self.csa_header.parsed, dict)
        self.assertIs(self.csa_header.parsed, self.csa_header.parsed)

    def test_n_slices_property(self):
        result = self.csa_header.n_slices
        expected = self.csa_header.parsed["SliceArray"]["Size"]
        self.assertEqual(result, expected)

