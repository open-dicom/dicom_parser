"""
Definition of the :class:`HeaderTestCase` class.
"""
import json
import warnings
from pathlib import Path
from unittest import TestCase

import pydicom
from dicom_parser.header import Header
from dicom_parser.utils.requires_pandas import _has_pandas
from dicom_parser.utils.sequence_detector import SequenceDetector
from dicom_parser.utils.value_representation import (
    ValueRepresentation,
    ValueRepresentationError,
)
from dicom_parser.utils.vr_to_data_element import get_data_element_class

from tests.fixtures import (
    SERIES_INSTANCE_UID,
    SOP_INSTANCE_UID,
    STUDY_INSTANCE_UID,
    TEST_FIELDS,
    TEST_GE_LOCALIZER_PATH,
    TEST_IMAGE_PATH,
    TEST_RSFMRI_IMAGE_PATH,
    TEST_SIEMENS_DWI_PATH,
)


class HeaderTestCase(TestCase):
    """
    Tests for the :class:`~dicom_parser.header.Header` class.
    """

    #: Valid keywords and matching values to test against.
    KEYWORDS = {
        "PatientID": "012345678",
        "SeriesInstanceUID": SERIES_INSTANCE_UID,
        "SOPInstanceUID": SOP_INSTANCE_UID,
        "StudyInstanceUID": STUDY_INSTANCE_UID,
        "StudyDate": "20180501",
    }

    #: Invalid keywords.
    NON_KEYWORDS = ["ABC", "DEF", "GHI", "JKL"]

    #: Valid tags and matching values to test against.
    TAGS = {
        (
            "0020",
            "000D",
        ): "1.3.12.2.1107.5.2.43.66024.30000018050107081466900000007",
        ("0008", "0060"): "MR",
        (
            "0020",
            "000E",
        ): "1.3.12.2.1107.5.2.43.66024.2018050112250992296484473.0.0.0",
        ("0028", "0030"): pydicom.multival.MultiValue(
            float, ["0.48828125", "0.48828125"]
        ),
    }

    #: Invalid tags.
    NON_TAGS = [
        ("1111", "0000"),
        ("0000", "1111"),
        ("2222", "3333"),
        ("3333", "4444"),
    ]

    #: Invalid types for data element query testing.
    BAD_DATA_ELEMENT_QUERY_VALUES = (
        0,
        ["1"],
        1.1,
        False,
        {"a": "b"},
        {1, 2, 3},
        None,
    )

    #: Strings to test the number of returned data elements for a
    #: `keyword_contains()` call.
    KEYWORD_CONTAINS = {"time": 10, "DATE": 7, "abcdef": 0}

    def setUp(self):
        self.raw = pydicom.dcmread(TEST_IMAGE_PATH)
        self.header = Header(self.raw)
        self.dwi_header = Header(TEST_SIEMENS_DWI_PATH)

    def test_str(self):
        value = str(self.header)
        self.assertIsInstance(value, str)

    def test_repr(self):
        value = repr(Header(TEST_RSFMRI_IMAGE_PATH))
        self.assertIsInstance(value, str)

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

    def test_initialized_with_default_sequence_detector(self):
        self.assertIsInstance(self.header.sequence_detector, SequenceDetector)

    def test_init_detected_sequence(self):
        self.assertEqual(self.header.detected_sequence, "localizer")

    def test_get_raw_element(self):
        keys = list(self.TAGS.keys()) + list(self.KEYWORDS.keys())
        for key in keys:
            result = self.header.get_raw_element(key)
            self.assertIsInstance(result, pydicom.DataElement)

    def test_get_raw_value_with_bad_type_raises_type_error(self):
        for invalid_key in self.BAD_DATA_ELEMENT_QUERY_VALUES:
            with self.assertRaises(TypeError):
                self.header.get_data_element(invalid_key)

    def test_get_data_element_with_bad_type_raises_type_error(self):
        for invalid_key in self.BAD_DATA_ELEMENT_QUERY_VALUES:
            with self.assertRaises(TypeError):
                self.header.get_raw_element(invalid_key)

    def test_get_raw_value(self):
        keys = list(self.TAGS.keys()) + list(self.KEYWORDS.keys())
        for key in keys:
            result = self.header.get_raw_value(key)
            self.assertNotIsInstance(result, pydicom.DataElement)
            expected = self.TAGS.get(key) or self.KEYWORDS.get(key)
            self.assertEqual(result, expected)

    def test_get_raw_value_with_invalid_key_raises_key_error(self):
        invalid_keys = self.NON_KEYWORDS + self.NON_TAGS
        for invalid_key in invalid_keys:
            with self.assertRaises(KeyError):
                self.header.get_raw_value(invalid_key)

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

    def test_get_default_parsed_configuration_is_true(self):
        parsed = TEST_FIELDS["StudyDate"]
        result = self.header.get("StudyDate")
        self.assertEqual(result, parsed)

    def test_indexing_operator_with_invalid_key_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.header["invalid_key"]

    def test_get_with_default_and_existing_key_return_key_value(self):
        expected = TEST_FIELDS["StudyDate"]
        result = self.header.get("StudyDate", "default value")
        self.assertEqual(result, expected)

    def test_get_with_default_and_missing_key_returns_default(self):
        default = "default value"
        result = self.header.get("invalid_key", default)
        self.assertEqual(result, default)

    def test_default_value_with_verbose_parse_true_and_existing_key(self):
        expected = TEST_FIELDS["StudyDate"]
        result = self.header.get("StudyDate", 0, parsed=True)
        self.assertEqual(result, expected)

    def test_default_value_with_verbose_parse_false_and_existing_key(self):
        expected = self.KEYWORDS["StudyDate"]
        result = self.header.get("StudyDate", 0, parsed=False)
        self.assertEqual(result, expected)

    def test_default_value_with_verbose_parse_true_and_missing_key(self):
        default = "default value"
        result = self.header.get("invalid_key", default, parsed=True)
        self.assertEqual(result, default)

    def test_default_value_with_verbose_parse_false_and_missing_key(self):
        default = "default value"
        result = self.header.get("invalid_key", default, parsed=False)
        self.assertEqual(result, default)

    def test_get_with_a_list_of_keywords(self):
        keywords = list(self.KEYWORDS)
        result = self.header.get(keywords, parsed=False)
        self.assertDictEqual(self.KEYWORDS, result)

    def test_get_with_a_list_of_tags(self):
        tags = list(self.TAGS)
        result = self.header.get(tags, parsed=False)
        self.assertDictEqual(self.TAGS, result)

    def test_get_with_a_mixed_list_of_tags_and_keywords(self):
        tags_and_keywords = list(self.TAGS) + list(self.KEYWORDS)
        expected = {**self.TAGS, **self.KEYWORDS}
        result = self.header.get(tags_and_keywords, parsed=False)
        self.assertDictEqual(result, expected)

    def test_get_with_a_csa_header_returns_dict(self):
        header = Header(TEST_IMAGE_PATH)
        result = header.get("CSASeriesHeaderInfo")
        self.assertIsInstance(result, dict)

    def test_get_with_a_missing_csa_header_returns_none(self):
        header = Header(TEST_GE_LOCALIZER_PATH)
        result = header.get("CSASeriesHeaderInfo")
        self.assertIsNone(result)

    def test_get_as_json(self):
        keys = list(self.TAGS.keys()) + list(self.KEYWORDS.keys())
        for key in keys:
            json_value = self.header.get(key, as_json=True)
            self.assertIsInstance(json_value, str)
            # Try to execute json.loads() just to make sure no exception is
            # raised.
            _ = json.loads(json_value)

    def test_detect_sequence(self):
        result = self.header.detect_sequence()
        expected = "localizer"
        self.assertEqual(result, expected)

    def test_detect_sequence_with_unknown_modality_returns_none(self):
        header = Header(TEST_IMAGE_PATH)
        header.raw.Modality = "UNKNOWN"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = header.detect_sequence()
        self.assertIsNone(result)

    def test_keyword_contains(self):
        for substring, expected in self.KEYWORD_CONTAINS.items():
            df = self.header.keyword_contains(substring)
            self.assertEqual(len(df), expected)

    def test_keyword_contains_exact(self):
        for substring, _ in self.KEYWORD_CONTAINS.items():
            df = self.header.keyword_contains(substring, exact=True)
            self.assertEqual(len(df), 0)
        for substring, expected in self.KEYWORD_CONTAINS.items():
            df = self.header.keyword_contains(substring.title())
            self.assertEqual(len(df), expected)

    def test_get_data_elements_with_vr_list(self):
        vr = [ValueRepresentation.IS, ValueRepresentation.CS]
        result = self.header.get_data_elements(value_representation=vr)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 20)

    def test_get_data_elements_with_vr_tuple(self):
        vr = ValueRepresentation.DA, ValueRepresentation.TM
        result = self.header.get_data_elements(value_representation=vr)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 13)

    def test_get_data_elements_with_exclude_list(self):
        exclude = [
            ValueRepresentation.IS,
            ValueRepresentation.CS,
            ValueRepresentation.DS,
            ValueRepresentation.UN,
        ]
        result = self.header.get_data_elements(exclude=exclude)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 59)

    def test_get_data_elements_with_exclude_tuple(self):
        exclude = ValueRepresentation.DA, ValueRepresentation.TM
        result = self.header.get_data_elements(exclude=exclude)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 120)

    def test_to_dataframe(self):
        if _has_pandas:
            import pandas as pd

            df = self.header.to_dataframe()
            self.assertIsInstance(df, pd.DataFrame)
        else:
            self.skipTest("pandas not installed")

    def test_to_dataframe_with_no_elements(self):
        if _has_pandas:
            import pandas as pd

            df = self.header.to_dataframe([])
            self.assertIsInstance(df, pd.DataFrame)
            self.assertTrue(df.empty)
        else:
            self.skipTest("pandas not installed")

    def test_to_dict(self):
        value = self.header.to_dict()
        self.assertIsInstance(value, dict)
        self.assertEqual(len(value), 120)

    def test_as_dict(self):
        value = self.header.as_dict
        expected = self.header.to_dict()
        self.assertIsInstance(value, dict)
        self.assertDictEqual(value, expected)

    def test_as_dict_is_cached(self):
        result_1 = self.header.as_dict
        result_2 = self.header.as_dict
        self.assertIs(result_1, result_2)

    def test_keys(self):
        value = self.header.keys
        self.assertIsInstance(value, list)
        self.assertEqual(len(value), 120)

    def test_unknown_value_representation(self):
        with self.assertRaises(ValueRepresentationError):
            get_data_element_class("invalid")

    def test_get_phase_encoding_direction(self):
        value = self.dwi_header.get_phase_encoding_direction()
        expected = "i-"
        self.assertEqual(value, expected)

    def test_get_phase_encoding_direction_with_none(self):
        ge_loc = Header(TEST_GE_LOCALIZER_PATH)
        value = ge_loc.get_phase_encoding_direction()
        self.assertIsNone(value)
