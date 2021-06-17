"""
Definition of the :class:`DateTestCase` class.
"""
from dicom_parser.data_elements.date import Date
from tests.test_data_element import DataElementTestCase


class DateTestCase(DataElementTestCase):
    """
    Tests for the :class:`~dicom_parser.data_elements.date.Date`
    class.
    """

    TEST_CLASS = Date
    SAMPLE_KEY = "StudyDate"

    def test_empty(self):
        original_value = self.raw_element.value
        self.raw_element.value = None
        element = self.TEST_CLASS(self.raw_element)
        self.assertIsNone(element.value)
        self.raw_element.value = ""
        element = self.TEST_CLASS(self.raw_element)
        self.assertIsNone(element.value)
        self.raw_element.value = False
        element = self.TEST_CLASS(self.raw_element)
        self.assertIsNone(element.value)
        self.raw_element.value = original_value

    def test_value_error(self):
        original_value = self.raw_element.value
        self.raw_element.value = "not_a_date"
        element = self.TEST_CLASS(self.raw_element)
        with self.assertRaises(ValueError):
            element.value
        self.raw_element.value = original_value

    def test_type_error(self):
        original_value = self.raw_element.value
        self.raw_element.value = ("why?",)
        element = self.TEST_CLASS(self.raw_element)
        with self.assertRaises(TypeError):
            element.value
        self.raw_element.value = original_value
