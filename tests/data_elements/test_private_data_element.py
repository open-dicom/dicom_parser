"""
Tests for the
:class:`~dicom_parser.data_elements.private_data_element.PrivateDataElement`
class.
"""
from dicom_parser.data_elements.private_data_element import PrivateDataElement
from tests.data_elements.fixtures import (
    PRIVATE_DATA_ELEMENTS,
    SIEMENS_DWI_ELEMENTS,
)
from tests.fixtures import TEST_SIEMENS_DWI_PATH
from tests.test_data_element import DataElementTestCase


class PrivateDataElementTestCase(DataElementTestCase):
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


class PrivateDataElementTestCase(PrivateDataElementTestCase):
    """
    Tests normal bytes encoded private data elements.
    """

    VALUES = PRIVATE_DATA_ELEMENTS


class SiemensTestCase(PrivateDataElementTestCase):
    """
    Tests private Siemens tags with custom parsing methods.
    """

    TEST_IMAGE = TEST_SIEMENS_DWI_PATH
    VALUES = SIEMENS_DWI_ELEMENTS
