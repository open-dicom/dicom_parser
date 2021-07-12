from pathlib import Path
from unittest import TestCase

import numpy as np
import pydicom
from dicom_parser.header import Header
from dicom_parser.image import Image

from tests.fixtures import (
    TEST_IMAGE_PATH,
    TEST_IMAGE_RELATIVE_PATH,
    TEST_RSFMRI_IMAGE_PATH,
)


class ImageTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.image = Image(TEST_IMAGE_PATH)
        cls.rsfmri_image = Image(TEST_RSFMRI_IMAGE_PATH)

    def test_initialization_with_string_path(self):
        image = Image(TEST_IMAGE_PATH)
        self.assertIsInstance(image, Image)
        self.assertIsInstance(image.header, Header)

    def test_initialization_with_pathlib_path(self):
        image = Image(Path(TEST_IMAGE_PATH))
        self.assertIsInstance(image, Image)
        self.assertIsInstance(image.header, Header)

    def test_initialization_with_filedataset(self):
        dataset = pydicom.dcmread(TEST_IMAGE_PATH)
        image = Image(dataset)
        self.assertIsInstance(image, Image)
        self.assertIsInstance(image.header, Header)

    def test_initialization_without_pixel_data_raises_attribute_error(self):
        dataset = pydicom.dcmread(TEST_IMAGE_PATH, stop_before_pixels=True)
        with self.assertWarns(Warning):
            Image(dataset)

    def test_image_position(self):
        value = self.image.position
        expected = (-39.605327606201, -148.57835578918, 94.533727645874)
        self.assertAlmostEqual(value, expected)

    def test_image_number(self):
        value = self.image.number
        expected = 1
        self.assertEqual(value, expected)

    def test_affine(self):
        value = self.image.affine
        expected = np.array(
            [
                [0.0, 0.0, 6.0, -39.60532761],
                [0.0, 0.48828125, -0.0, -148.57835579],
                [-0.48828125, 0.0, 0.0, 94.53372765],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )
        self.assertTrue(np.allclose(value, expected))

    def test_affine_with_missing(self):
        original_value = self.image.header.raw["ImageOrientationPatient"].value
        self.image.header.raw["ImageOrientationPatient"].value = None
        value = self.image.affine
        self.assertIsNone(value)
        self.image.header.raw["ImageOrientationPatient"].value = original_value

    def test_is_rsfmri_property(self):
        self.assertFalse(self.image.is_fmri)
        self.assertTrue(self.rsfmri_image.is_fmri)

    def test_regular_2d_image_returns_raw_pixel_array(self):
        expected = self.image._data
        self.assertTrue(np.array_equal(self.image.data, expected))

    def test_is_mosaic_property(self):
        not_mosaic_image = Image(TEST_IMAGE_PATH)
        self.assertFalse(not_mosaic_image.is_mosaic)
        mosaic_image = Image(TEST_RSFMRI_IMAGE_PATH)
        self.assertTrue(mosaic_image.is_mosaic)

    def test_siemens_mosaic_returns_as_volume(self):
        n_dimensions = self.rsfmri_image.data.ndim
        expected = 3
        self.assertEqual(n_dimensions, expected)

    def test_siemens_mosaic_returns_with_expected_shape(self):
        shape = self.rsfmri_image.data.shape
        expected = 96, 96, 64
        self.assertEqual(shape, expected)

    def test_get_default_relative_path(self):
        value = self.image.get_default_relative_path()
        expected = TEST_IMAGE_RELATIVE_PATH
        self.assertEqual(value, expected)

    def test_default_relative_path(self):
        value = self.image.default_relative_path
        expected = TEST_IMAGE_RELATIVE_PATH
        self.assertEqual(value, expected)

    def test_image_shape(self):
        value = self.image.image_shape
        expected = (512, 512)
        self.assertTupleEqual(value, expected)

    def test_image_shape_with_missing(self):
        self.image.header.raw["Rows"].value = None
        value = self.image.image_shape
        self.assertIsNone(value)
        self.image.header.raw["Rows"].value = 512

    def test_image_orientation_patient(self):
        value = self.image.image_orientation_patient
        expected = np.array([[0, 0], [1, 0], [0, -1]])
        self.assertTrue(np.array_equal(value, expected))

    def test_image_orientation_patient_missing(self):
        original_value = self.image.header.raw["ImageOrientationPatient"].value
        self.image.header.raw["ImageOrientationPatient"].value = None
        value = self.image.image_orientation_patient
        self.assertIsNone(value)
        self.image.header.raw["ImageOrientationPatient"].value = original_value

    def test_slice_normal(self):
        value = self.image.slice_normal
        expected = np.array([1.0, -0.0, 0.0])
        self.assertTrue(np.array_equal(value, expected))

    def test_slice_normal_missing(self):
        original_value = self.image.header.raw["ImageOrientationPatient"].value
        self.image.header.raw["ImageOrientationPatient"].value = None
        value = self.image.slice_normal
        self.assertIsNone(value)
        self.image.header.raw["ImageOrientationPatient"].value = original_value

    def test_rotation_matrix(self):
        value = self.image.rotation_matrix
        expected = [[0, 0, 1], [0, 1, -0.0], [-1, 0, 0]]
        self.assertTrue(np.array_equal(value, expected))

    def test_rotation_matrix_missing(self):
        original_value = self.image.header.raw["ImageOrientationPatient"].value
        self.image.header.raw["ImageOrientationPatient"].value = None
        value = self.image.rotation_matrix
        self.assertIsNone(value)
        self.image.header.raw["ImageOrientationPatient"].value = original_value

    def test_spatial_resolution(self):
        value = self.image.spatial_resolution
        expected = (0.48828125, 0.48828125, 6.0)
        self.assertTupleEqual(value, expected)

    def test_spatial_resolution_without_thickness(self):
        original_value = self.image.header.raw["SliceThickness"].value
        self.image.header.raw["SliceThickness"].value = None
        value = self.image.spatial_resolution
        expected = (0.48828125, 0.48828125)
        self.assertTupleEqual(value, expected)
        self.image.header.raw["SliceThickness"].value = original_value
