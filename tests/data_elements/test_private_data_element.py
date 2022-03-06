"""
Tests for the
:class:`~dicom_parser.data_elements.private_data_element.PrivateDataElement`
class.
"""
from dicom_parser.data_elements.private_data_element import PrivateDataElement
from tests.data_elements.fixtures import (
    PRIVATE_DATA_ELEMENTS,
    SIEMENS_DWI_ELEMENTS,
    SIEMENS_EXPLICIT_VR_ELEMENTS,
)
from tests.fixtures import TEST_SIEMENS_DWI_PATH, TEST_SIEMENS_EXPLICIT_VR
from tests.test_data_element import DataElementTestCase


class PrivateDataElementTestCaseBase(DataElementTestCase):
    """
    Base class for private data element tests.
    """

    TEST_CLASS = PrivateDataElement

    def get_raw_element(self, key):
        """
        Override parent method to use brackets, otherwise pydicom raises an
        exception for private tags.
        """
        return self.raw_header[key]

    def test_is_public(self):
        if self.TEST_CLASS is None or self.SAMPLE_KEY == "":
            self.skipTest(self.SKIP_MESSAGE)
        element = self.TEST_CLASS(self.raw_element)
        self.assertFalse(element.is_public)

    def test_is_private(self):
        if self.TEST_CLASS is None or self.SAMPLE_KEY == "":
            self.skipTest(self.SKIP_MESSAGE)
        element = self.TEST_CLASS(self.raw_element)
        self.assertTrue(element.is_private)


class PrivateDataElementTestCase(PrivateDataElementTestCaseBase):
    """
    Tests normal bytes encoded private data elements.
    """

    VALUES = PRIVATE_DATA_ELEMENTS


class SiemensTestCase(PrivateDataElementTestCaseBase):
    """
    Tests private Siemens tags with custom parsing methods.
    """

    TEST_IMAGE = TEST_SIEMENS_DWI_PATH
    VALUES = SIEMENS_DWI_ELEMENTS


class SiemensExplicitVRTestCase(PrivateDataElementTestCase):
    """
    Tests private Siemens tags with custom parsing methods when an expicit VR
    is specified for the private tags in the other.
    """

    TEST_IMAGE = TEST_SIEMENS_EXPLICIT_VR
    VALUES = SIEMENS_EXPLICIT_VR_ELEMENTS

    BANDWIDTH_PER_PIXEL_TAG = (0x19, 0x1028)
    ACQISITION_TIMES_TAG = (0x19, 0x1029)
    N_IMAGES_TAG = (0x19, 0x100A)

    def test_mosaic_acquisition_times_bad_type(self):
        """
        Checks that a ValueError is raised for non bytes or float
        MosaicRefAcqTimes values.
        """
        tag = self.ACQISITION_TIMES_TAG
        self.header.raw[tag].value = 3
        with self.assertRaises(TypeError):
            self.header.get_data_element(tag).value # pylint: disable=W0106

    def test_n_images_in_mosaic_bad_type(self):
        """
        Checks that a ValueError is raised for non bytes or int
        NumberOfImagesInMosaic values.
        """
        tag = self.N_IMAGES_TAG
        self.header.raw[tag].value = 3.0
        with self.assertRaises(TypeError):
            self.header.get_data_element(tag).value # pylint: disable=W0106

    def test_badwidth_per_pixel_phase_encode_bad_type(self):
        """
        Checks that a ValueError is raised for non bytes or float
        MosaicRefAcqTimes values.
        """
        tag = self.BANDWIDTH_PER_PIXEL_TAG
        self.header.raw[tag].value = "?"
        with self.assertRaises(TypeError):
            self.header.get_data_element(tag).value # pylint: disable=W0106
