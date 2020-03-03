import nibabel as nib
import numpy as np

from dicom_parser.image import Image
from dicom_parser.utils.siemens.mosaic import Mosaic
from tests.fixtures import (
    TEST_RSFMRI_IMAGE_PATH,
    TEST_RSFMRI_IMAGE_VOLUME,
    TEST_RSFMRI_SERIES_NIFTI,
)
from unittest import TestCase


class MosaicTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.image = Image(TEST_RSFMRI_IMAGE_PATH)
        cls.mosaic = Mosaic(cls.image._data, cls.image.header)

    def test_init_read_series_header_info(self):
        csa_header = self.mosaic.series_header_info
        self.assertIsInstance(csa_header, dict)

    def test_init_read_volume_shape(self):
        value = self.mosaic.volume_shape
        expected = 96, 96, 64
        self.assertTupleEqual(value, expected)

    def test_init_read_mosaic_dimensions(self):
        value = self.mosaic.mosaic_dimensions
        expected = 8, 8
        self.assertTupleEqual(value, expected)

    def test_ascending_attribute_with_ascending(self):
        value = self.mosaic.ascending
        self.assertTrue(value)

    # TODO: Find descending mosaic to test with
    # def test_ascending_attribute_with_descending(self):
    #     value = self.mosaic.ascending
    #     self.assertFalse(value)

    def test_folded_data(self):
        volume = self.mosaic.fold()
        expected = np.load(TEST_RSFMRI_IMAGE_VOLUME)
        self.assertTrue(np.array_equal(volume, expected))

    def test_folded_data_is_same_as_nifti(self):
        volume = self.mosaic.fold()
        nii_data = np.asanyarray(nib.load(TEST_RSFMRI_SERIES_NIFTI).dataobj)
        nii_volume = nii_data[:, :, :, 0]
        self.assertTrue(np.array_equal(volume, nii_volume))
