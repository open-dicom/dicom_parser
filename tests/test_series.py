import nibabel as nib
import numpy as np

from dicom_parser.image import Image
from dicom_parser.series import Series
from pathlib import Path
from tests.fixtures import (
    TEST_IMAGE_PATH,
    TEST_RSFMRI_SERIES_PATH,
    TEST_RSFMRI_SERIES_NIFTI,
    TEST_SERIES_PATH,
    TEST_UTILS_DIRECTORY,
)
from unittest import TestCase


class SeriesTestCase(TestCase):
    def setUp(self):
        self.localizer = Series(TEST_SERIES_PATH)

    def test_initialization_with_string_path(self):
        series = Series(TEST_SERIES_PATH)
        self.assertIsInstance(series, Series)
        self.assertIsInstance(series.path, Path)
        self.assertIsInstance(series.images, tuple)

    def test_initialization_with_pathlib_path(self):
        series = Series(Path(TEST_SERIES_PATH))
        self.assertIsInstance(series, Series)
        self.assertIsInstance(series.path, Path)
        self.assertIsInstance(series.images, tuple)

    def test_initialization_with_file_path_raises_value_error(self):
        with self.assertRaises(ValueError):
            Series(TEST_IMAGE_PATH)

    def test_initialization_with_invalid_path_raises_value_error(self):
        with self.assertRaises(ValueError):
            Series("/some/invalid_path/at/nowhere")

    def test_initialization_with_no_dcms_in_path_raises_file_not_found_error(self):
        with self.assertRaises(FileNotFoundError):
            Series(TEST_UTILS_DIRECTORY)

    def test_get_images_got_correct_number_of_images(self):
        series = Series(TEST_SERIES_PATH)
        self.assertEqual(len(series.images), 11)

    def test_images_are_ordered_by_instance_number(self):
        series = Series(TEST_SERIES_PATH)
        instance_numbers = tuple(
            [image.header.get("InstanceNumber") for image in series.images]
        )
        expected = tuple(range(1, 12))
        self.assertTupleEqual(instance_numbers, expected)

    def test_data_property(self):
        series = Series(TEST_SERIES_PATH)
        self.assertIsInstance(series.data, np.ndarray)
        self.assertTupleEqual(series.data.shape, (512, 512, 11))

    def test_mosaic_series_returns_as_4d(self):
        series = Series(TEST_RSFMRI_SERIES_PATH)
        data = series.data
        expected_shape = 96, 96, 64, 3
        self.assertTupleEqual(data.shape, expected_shape)

    def test_mosaic_series_data_same_as_nifti(self):
        series = Series(TEST_RSFMRI_SERIES_PATH)
        nii_data = np.asanyarray(nib.load(TEST_RSFMRI_SERIES_NIFTI).dataobj)
        self.assertTrue(np.array_equal(series.data, nii_data))

    def test_len(self):
        rsfmri = Series(TEST_RSFMRI_SERIES_PATH)
        self.assertEqual(len(self.localizer), 11)
        self.assertEqual(len(rsfmri), 3)

    def test_get_method_with_single_value_keyword(self):
        result = self.localizer.get("EchoTime")
        expected = 3.04
        self.assertEqual(result, expected)

    def test_get_method_with_single_value_tuple(self):
        result = self.localizer.get(("0018", "0080"))
        expected = 7.6
        self.assertEqual(result, expected)

    def test_get_method_with_multiple_values_keyword(self):
        result = self.localizer.get("InstanceNumber")
        expected = list(range(1, 12))
        self.assertListEqual(result, expected)

    def test_get_method_with_multiple_values_tuple(self):
        result = self.localizer.get(("0008", "0018"))
        expected = [
            "1.3.12.2.1107.5.2.43.66024.2018012410454373581200543",
            "1.3.12.2.1107.5.2.43.66024.201801241046013643300561",
            "1.3.12.2.1107.5.2.43.66024.2018012410454348504800541",
            "1.3.12.2.1107.5.2.43.66024.2018012410460458489400565",
            "1.3.12.2.1107.5.2.43.66024.2018012410454687305600545",
            "1.3.12.2.1107.5.2.43.66024.2018012410460815771100569",
            "1.3.12.2.1107.5.2.43.66024.2018012410455043640800549",
            "1.3.12.2.1107.5.2.43.66024.2018012410461190213200575",
            "1.3.12.2.1107.5.2.43.66024.2018012410455394762200553",
            "1.3.12.2.1107.5.2.43.66024.2018012410461517027500577",
            "1.3.12.2.1107.5.2.43.66024.2018012410455755378100557",
        ]
        self.assertListEqual(result, expected)

    def test_get_method_with_missing_keyword(self):
        result = self.localizer.get("MissingKey")
        self.assertIsNone(result)

    def test_get_method_with_missing_keyword_and_default(self):
        result = self.localizer.get("MissingKey", "default_value")
        expected = "default_value"
        self.assertEqual(result, expected)

    def test_indexing_operator_with_string(self):
        result = self.localizer["EchoTime"]
        expected = 3.04
        self.assertEqual(result, expected)

    def test_indexing_operator_with_tag_and_multiple_values(self):
        result = self.localizer[("0020", "0013")]
        expected = list(range(1, 12))
        self.assertListEqual(result, expected)

    def test_indexing_operator_with_int_returns_image_instance(self):
        result = self.localizer[3]
        self.assertIsInstance(result, Image)

    def test_indexing_operator_with_int_returns_correct_instance(self):
        result = self.localizer[3].header.get("InstanceNumber")
        self.assertEqual(result, 4)

    def test_indexing_operator_with_slice_returns_multiple_images(self):
        result = self.localizer[3:6]
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)

    def test_indexing_operator_with_invalid_key_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.localizer["MissingKey"]

    def test_indexing_operator_with_invalid_type_raises_type_error(self):
        invalid_types = True, 4.20, b"bytes", [1, 2, 3]
        for value_type in invalid_types:
            with self.assertRaises(TypeError):
                self.localizer[value_type]
