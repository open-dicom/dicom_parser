import pydicom

from dicom_parser.utils.siemens.csa.data_element import CsaDataElement
from dicom_parser.utils.siemens.csa.header import CsaHeader
from dicom_parser.utils.siemens.private_tags import SIEMENS_PRIVATE_TAGS
from tests.fixtures import TEST_RSFMRI_IMAGE_PATH
from tests.utils.siemens.csa.fixtures import (
    ARRAY_PATTERNS,
    LISTED_KEYS,
    NON_ARRAY_PATTERNS,
    RAW_ELEMENTS,
    VALUES,
)
from unittest import TestCase


class CsaDataElementTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        dcm = pydicom.dcmread(TEST_RSFMRI_IMAGE_PATH)
        tag = SIEMENS_PRIVATE_TAGS["CSASeriesHeaderInfo"]
        cls.series_header_info = dcm.get(tag).value
        cls.csa_header = CsaHeader(cls.series_header_info)
        cls.csa_data_element = CsaDataElement(cls.csa_header.raw_elements[0])

    def test_init_splits_to_key_and_value(self):
        first_key = ["Version"]
        first_value = "51130001"
        self.assertListEqual(self.csa_data_element.key, first_key)
        self.assertEqual(self.csa_data_element.value, first_value)
        element_100 = CsaDataElement(self.csa_header.raw_elements[100])
        key_100 = ["GRADSPEC", "GPAData[0]", "EddyCompensationY", "TimeConstant[1]"]
        value_100 = "0.917683601379"
        self.assertListEqual(element_100.key, key_100)
        self.assertEqual(element_100.value, value_100)

    def test_clean_part(self):
        raw_part_names = "sSliceArray", "lTrackingBackgroundSuppr", "alRecoveryDuration"
        expected = "SliceArray", "TrackingBackgroundSuppr", "RecoveryDuration"
        for i, raw_part_name in enumerate(raw_part_names):
            clean_part = self.csa_data_element.clean_part(raw_part_name)
            self.assertEqual(clean_part, expected[i])

    def test_key_to_list(self):
        key_sample = [raw_element.split("\t")[0] for raw_element in RAW_ELEMENTS]
        for key, expected in zip(key_sample, LISTED_KEYS):
            result = self.csa_data_element.key_to_list(key)
            self.assertListEqual(result, expected)

    def test_split(self):
        for i, raw_element in enumerate(RAW_ELEMENTS):
            data_element = CsaDataElement(raw_element)
            key, value = data_element.split()
            self.assertListEqual(key, LISTED_KEYS[i])
            self.assertEqual(value, VALUES[i])

    def test_search_array_pattern(self):
        for array_pattern in ARRAY_PATTERNS:
            result = self.csa_data_element.search_array_pattern(array_pattern)
            self.assertIsInstance(result, int)
        for non_array_pattern in NON_ARRAY_PATTERNS:
            result = self.csa_data_element.search_array_pattern(non_array_pattern)
            self.assertIsNone(result)

