"""
Definition of the :class:`IntegerStringTestCase` class.
"""
from dicom_parser.data_elements.integer_string import IntegerString
from tests.test_data_element import DataElementTestCase


class IntegerStringTestCase(DataElementTestCase):
    """
    Tests for the
    :class:`~dicom_parser.data_elements.integer_string.IntegerString`
    class.
    """

    TEST_CLASS = IntegerString
    SAMPLE_KEY = "InstanceNumber"

    def test_empty(self):
        original_value = self.raw_element.value
        self.raw_element.value = ""
        element = self.TEST_CLASS(self.raw_element)
        self.assertIsNone(element.value)
        self.raw_element.value = original_value
