from pathlib import Path
from unittest import TestCase

import numpy as np
import pydicom
from dicom_parser.header import Header
from dicom_parser.image import Image
from dicom_parser.utils.multi_frame.multi_frame import MultiFrame
from dicom_parser.utils.siemens.mosaic import Mosaic

from tests.fixtures import (TEST_IMAGE_PATH, TEST_IMAGE_RELATIVE_PATH,
                            TEST_MULTIFRAME, TEST_RSFMRI_IMAGE_PATH,
                            TEST_SIEMENS_DWI_PATH)


class ImageTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rsfmri_image = Image(TEST_RSFMRI_IMAGE_PATH)
        cls.siemens_dwi = Image(TEST_SIEMENS_DWI_PATH)
        cls.multi_frame = Image(TEST_MULTIFRAME)

    def setUp(self):
        self.image = Image(TEST_IMAGE_PATH)

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
        value = self.image.image_position
        expected = (-39.605327606201, -148.57835578918, 94.533727645874)
        self.assertAlmostEqual(value, expected)

    def test_mosaic_image_position(self):
        value = self.siemens_dwi.image_position
        expected = np.array([-15.45403804, -107.76991802, 80.05488457])
        self.assertTrue(np.allclose(value, expected))

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

    def test_is_fmri_property(self):
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

    def test_mosaic_property_with_mosaic(self):
        self.assertIsInstance(self.rsfmri_image.mosaic, Mosaic)

    def test_mosaic_property_with_non_mosaic(self):
        self.assertIsNone(self.image.mosaic)
        self.assertIsNone(self.multi_frame.mosaic)

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

    def test_mosaic_image_shape(self):
        value = self.siemens_dwi.image_shape
        expected = (128, 128, 9)
        self.assertTupleEqual(value, expected)

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

    def test_mosaic_image_orientation_patient(self):
        value = self.siemens_dwi.image_orientation_patient
        expected = np.array(
            [
                [-3.41585276e-02, 3.14874388e-02],
                [9.99416427e-01, 1.07615111e-03],
                [-4.14689430e-08, -9.99503568e-01],
            ]
        )
        self.assertTrue(np.allclose(value, expected))

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

    def test_b_matrix(self):
        value = self.siemens_dwi.b_matrix
        expected = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        self.assertTrue(np.array_equal(value, expected))

    def test_b_matrix_with_missing(self):
        value = self.image.b_matrix
        self.assertIsNone(value)

    def test_voxel_space_b_matrix(self):
        value = self.siemens_dwi.voxel_space_b_matrix
        expected = np.array(
            [
                [0.93497292, -0.93334641, -1.02937305],
                [-0.93334641, 0.93172273, 1.02758232],
                [-1.02937305, 1.02758232, 1.13330435],
            ]
        )
        self.assertTrue(np.allclose(value, expected))

    def test_voxel_space_b_matrix_with_missing(self):
        value = self.image.voxel_space_b_matrix
        self.assertIsNone(value)

    def test_q_vector(self):
        value = self.siemens_dwi.q_vector
        expected = np.array([1.67478917, -1.67187565, -1.84388531])
        self.assertTrue(np.allclose(value, expected))

    def test_q_vector_with_missing(self):
        value = self.image.q_vector
        self.assertIsNone(value)

    def test_b_vector(self):
        value = self.siemens_dwi.b_vector
        expected = np.array([0.55826306, -0.55729188, -0.61462844])
        self.assertTrue(np.allclose(value, expected))

    def test_b_vector_with_missing(self):
        value = self.image.b_vector
        self.assertIsNone(value)

    def test_multiframe_property_with_multi_frame(self):
        self.assertIsInstance(self.multi_frame.multi_frame, MultiFrame)

    def test_multiframe_property_with_non_multi_frame(self):
        self.assertIsNone(self.image.multi_frame)
        self.assertIsNone(self.rsfmri_image.multi_frame)
        self.assertIsNone(self.siemens_dwi.multi_frame)

    def test_data_returned_with_missing_image_type(self):
        del self.image.header.raw["ImageType"]
        try:
            self.image.data
        except Exception as e:
            self.fail(
                f"Exception raised retreiving data for an image with a missing ImageType header field: {e}"  # noqa: E501
            )

    def test_image_with_no_data_returns_none(self):
        self.image._data = None
        value = self.image.data
        self.assertIsNone(value)
