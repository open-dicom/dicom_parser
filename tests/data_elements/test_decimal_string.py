"""
Definition of the :class:`DecimalStringTestCase` class.
"""
from dicom_parser.data_elements.decimal_string import DecimalString
from tests.test_data_element import DataElementTestCase


class DecimalStringTestCase(DataElementTestCase):
    """
    Tests for the
    :class:`~dicom_parser.data_elements.decimal_string.DecimalString`
    class.
    """

    TEST_CLASS = DecimalString
    SAMPLE_KEY = "PatientSize"

    def test_empty(self):
        original_value = self.raw_element.value
        self.raw_element.value = ""
        element = self.TEST_CLASS(self.raw_element)
        self.assertIsNone(element.value)
        self.raw_element.value = original_value
