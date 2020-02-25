import nibabel as nib
import numpy as np

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
