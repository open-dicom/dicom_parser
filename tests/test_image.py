import pydicom

from dicom_parser.header import Header
from dicom_parser.image import Image
from pathlib import Path
from tests.fixtures import TEST_IMAGE_PATH
from unittest import TestCase


class ImageTestCase(TestCase):
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
        with self.assertRaises(AttributeError):
            Image(dataset)
