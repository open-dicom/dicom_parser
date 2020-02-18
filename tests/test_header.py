import pydicom

from dicom_parser.parser import Parser
from dicom_parser.header import Header
from pathlib import Path
from tests.fixtures import TEST_IMAGE_PATH, TEST_STUDY_FIELDS
from unittest import TestCase


class HeaderTestCase(TestCase):
    KEYWORDS = {
        "PatientID": "304848286",
        "SeriesInstanceUID": "1.3.12.2.1107.5.2.43.66024.2018050112250992296484473.0.0.0",
        "SOPInstanceUID": "1.3.12.2.1107.5.2.43.66024.2018050112252318571884482",
        "StudyInstanceUID": "1.3.12.2.1107.5.2.43.66024.30000018050107081466900000007",
        "StudyDate": "20180501",
    }
    NON_KEYWORDS = ["ABC", "DEF", "GHI", "JKL"]
    TAGS = {
        ("0020", "000D"): "1.3.12.2.1107.5.2.43.66024.30000018050107081466900000007",
        ("0008", "0060"): "MR",
        ("0020", "000E"): "1.3.12.2.1107.5.2.43.66024.2018050112250992296484473.0.0.0",
        ("0028", "0030"): pydicom.multival.MultiValue(
            float, ["0.48828125", "0.48828125"]
        ),
    }
    NON_TAGS = [("1111", "0000"), ("0000", "1111"), ("2222", "3333"), ("3333", "4444")]

    @classmethod
    def setUpClass(cls):
        cls.raw = pydicom.read_file(TEST_IMAGE_PATH, stop_before_pixels=True)
        cls.header = Header(cls.raw)

    def test_instantiation_with_filedataset(self):
        self.assertIsInstance(self.header.raw, pydicom.FileDataset)

    def test_instantiation_with_string_path(self):
        header = Header(TEST_IMAGE_PATH)
        self.assertIsInstance(header.raw, pydicom.FileDataset)

    def test_instantiation_with_path_instance(self):
        path = Path(TEST_IMAGE_PATH)
        header = Header(path)
        self.assertIsInstance(header.raw, pydicom.FileDataset)

    def test_incorrect_raw_input_raises_type_error(self):
        bad_inputs = 6, 4.2, ("/some/path",), ["/another/path"], None
        for bad_input in bad_inputs:
            with self.assertRaises(TypeError):
                Header(bad_input)

    def test_initialized_with_default_parser(self):
        self.assertIsInstance(self.header.parser, Parser)

    def test_get_element_by_keyword(self):
        for keyword in self.KEYWORDS.keys():
            result = self.header.get_element_by_keyword(keyword)
            self.assertIsInstance(result, pydicom.DataElement)

    def test_get_element_by_keyword_invalid_key_returns_none(self):
        for keyword in self.NON_KEYWORDS:
            result = self.header.get_element_by_keyword(keyword)
            self.assertIsNone(result)

    def test_get_element_by_tag(self):
        for tag in self.TAGS.keys():
            result = self.header.get_element_by_tag(tag)
            self.assertIsInstance(result, pydicom.DataElement)

    def test_get_element_by_tag_invalid_tag_returns_none(self):
        for invalid_tag in self.NON_TAGS:
            result = self.header.get_element_by_tag(invalid_tag)
            self.assertIsNone(result)

    def test_get_element(self):
        keys = list(self.TAGS.keys()) + list(self.KEYWORDS.keys())
        for key in keys:
            result = self.header.get_element(key)
            self.assertIsInstance(result, pydicom.DataElement)

    def test_get_element_with_invalid_key_or_tag_return_none(self):
        for key in self.NON_TAGS + self.NON_KEYWORDS + [1]:
            result = self.header.get_element(key)
            self.assertIsNone(result)

    def test_get_raw_value(self):
        keys = list(self.TAGS.keys()) + list(self.KEYWORDS.keys())
        for key in keys:
            result = self.header.get_raw_value(key)
            self.assertNotIsInstance(result, pydicom.DataElement)
            expected = self.TAGS.get(key) or self.KEYWORDS.get(key)
            self.assertEqual(result, expected)

    def test_get_raw_value_with_invalid_key_returns_none(self):
        invalid_keys = self.NON_KEYWORDS + self.NON_TAGS
        for invalid_key in invalid_keys:
            result = self.header.get_raw_value(invalid_key)
            self.assertIsNone(result)

    def test_get_parsed_value(self):
        expected_study_date = TEST_STUDY_FIELDS["date"]
        study_date = self.header.get_parsed_value("StudyDate")
        expected_pixel_spacing = [
            float(value) for value in self.header.get_raw_value("PixelSpacing")
        ]
        pixel_spacing = self.header.get_parsed_value("PixelSpacing")
        self.assertEqual(study_date, expected_study_date)
        self.assertEqual(pixel_spacing, expected_pixel_spacing)

    def test_get(self):
        keys = list(self.TAGS.keys()) + list(self.KEYWORDS.keys())
        for key in keys:
            raw = self.header.get_raw_value(key)
            parsed = self.header.get_parsed_value(key)
            raw_result = self.header.get(key, parsed=False)
            parsed_result = self.header.get(key, parsed=True)
            self.assertEqual(raw_result, raw)
            self.assertEqual(parsed_result, parsed)

    def test_get_with_invalid_key_returns_none(self):
        invalid_keys = self.NON_KEYWORDS + self.NON_TAGS
        for invalid_key in invalid_keys:
            result = self.header.get(invalid_key)
            self.assertIsNone(result)

    def test_get_default_configuration(self):
        raw = self.KEYWORDS["StudyDate"]
        parsed = TEST_STUDY_FIELDS["date"]
        result = self.header.get("StudyDate")
        self.assertEqual(result, parsed)
        self.assertNotEqual(result, raw)

