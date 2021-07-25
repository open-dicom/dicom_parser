"""
Tests for the :class:`dicom_parser.utils.multi_frame.multi_frame.MultiFrame`
class.

TODO
----
* Test series signature.
* Test properties return cached values.
* Find multi-stack multi-frame image to test NotImplementedError.
* Find Phillips image with a derived appendix to test exclusion in frames info.
* Find 3D multi-frame to test.
"""
from unittest import TestCase

import numpy as np
from dicom_parser.image import Image
from dicom_parser.utils.exceptions import DicomParsingError
from dicom_parser.utils.multi_frame import MultiFrame
from tests.fixtures import TEST_MULTIFRAME


class MultiFrameTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.image = Image(TEST_MULTIFRAME)
        cls.multi_frame = MultiFrame(cls.image._data, cls.image.header)

    def test_image_shape(self):
        value = self.multi_frame.image_shape
        expected = (512, 512, 56, 2)
        self.assertTupleEqual(value, expected)

    def test_image_position(self):
        value = self.multi_frame.image_position
        expected = np.array([-163.2, 93.3, 195.8])
        self.assertTrue(np.array_equal(value, expected))

    def test_voxel_sizes(self):
        value = self.multi_frame.voxel_sizes
        expected = (0.625, 0.625, 3.0)
        self.assertTupleEqual(value, expected)

    def test_image_orientation_patient(self):
        value = self.multi_frame.image_orientation_patient
        expected = np.array([[1.0, 0.0], [0.0, 0.0], [0.0, -1.0]])
        self.assertTrue(np.array_equal(value, expected))

    def test_get_data(self):
        value = self.multi_frame.get_data()
        scaled = self.image.data  # Scaling is meaningless in our test
        expected = np.load(TEST_MULTIFRAME.replace("dcm", "npy"))
        self.assertTrue(np.array_equal(value, expected))
        self.assertTrue(np.array_equal(scaled, expected))

    def test_bad_n_frames(self):
        original_value = self.image.header["NumberOfFrames"]
        self.image.header.raw["NumberOfFrames"].value = 100
        bad_mf = MultiFrame(self.image._data, self.image.header)
        with self.assertRaises(DicomParsingError):
            bad_mf.get_data()
        self.image.header.raw["NumberOfFrames"].value = original_value

    def test_image_shape_with_missing_rows(self):
        original_value = self.image.header["Rows"]
        self.image.header.raw["Rows"].value = None
        bad_mf = MultiFrame(self.image._data, self.image.header)
        self.assertIsNone(bad_mf.image_shape)
        self.image.header.raw["Rows"].value = original_value

    def test_get_data_with_missing_rows(self):
        original_value = self.image.header["Rows"]
        self.image.header.raw["Rows"].value = None
        bad_mf = MultiFrame(self.image._data, self.image.header)
        with self.assertRaises(DicomParsingError):
            bad_mf.get_data()
        self.image.header.raw["Rows"].value = original_value

    def test_image_shape_with_missing_columns(self):
        original_value = self.image.header["Columns"]
        self.image.header.raw["Columns"].value = None
        bad_mf = MultiFrame(self.image._data, self.image.header)
        self.assertIsNone(bad_mf.image_shape)
        self.image.header.raw["Columns"].value = original_value

    def test_get_data_with_missing_columns(self):
        original_value = self.image.header["Columns"]
        self.image.header.raw["Columns"].value = None
        bad_mf = MultiFrame(self.image._data, self.image.header)
        with self.assertRaises(DicomParsingError):
            bad_mf.get_data()
        self.image.header.raw["Columns"].value = original_value

    def test_get_scaling_parameters(self):
        value = self.multi_frame.get_scaling_parameters()
        expected = (1, 0)
        self.assertTupleEqual(value, expected)
