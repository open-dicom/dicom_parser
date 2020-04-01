import numpy as np
import pydicom

from dicom_parser.header import Header
from dicom_parser.image import Image
from pathlib import Path
from tests.fixtures import TEST_IMAGE_PATH, TEST_RSFMRI_IMAGE_PATH
from unittest import TestCase


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
