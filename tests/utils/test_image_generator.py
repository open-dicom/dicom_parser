"""
Tests for the :mod:`dicom_parser.utils.image_generator` module.
"""
from pathlib import Path
from unittest import TestCase

from dicom_parser.utils.image_generator import generate_images
from tests.fixtures import TEST_SERIES_PATH


class ImageGeneratorTestCase(TestCase):
    def setUp(self) -> None:
        self.series_path = Path(TEST_SERIES_PATH)
        return super().setUp()

    def test_default_extensions_filtering(self):
        paths = tuple(generate_images(self.series_path))
        self.assertEqual(len(paths), 12)

    def test_custom_extensions_filtering(self):
        paths = tuple(generate_images(self.series_path, extension=(".ima",)))
        self.assertEqual(len(paths), 1)

    def test_allow_empty(self):
        try:
            generate_images(
                self.series_path, extension=(".???",), allow_empty=True
            )
        except FileNotFoundError:
            self.fail("FileNotFoundError raised with allow_empty!")
