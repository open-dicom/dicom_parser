"""
Definition of the :class:`AgeStringTestCase` class.
"""
from dicom_parser.data_elements.age_string import AgeString
from tests.test_data_element import DataElementTestCase


class AgeStringTestCase(DataElementTestCase):
    """
    Tests for the :class:`~dicom_parser.data_elements.age_string.AgeString`
    class.
    """

    TEST_CLASS = AgeString
    SAMPLE_KEY = "PatientAge"

    def test_empty(self):
        original_value = self.raw_element.value
        self.raw_element.value = ""
        element = self.TEST_CLASS(self.raw_element)
        self.assertIsNone(element.value)
        self.raw_element.value = original_value
