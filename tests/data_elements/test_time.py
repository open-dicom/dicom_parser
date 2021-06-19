"""
Definition of the :class:`TimeTestCase` class.
"""
import datetime

from dicom_parser.data_elements.time import Time
from tests.test_data_element import DataElementTestCase


class TimeTestCase(DataElementTestCase):
    """
    Tests for the :class:`~dicom_parser.data_elements.time.Time`
    class.
    """

    TEST_CLASS = Time
    SAMPLE_KEY = "StudyTime"

    def test_empty(self):
        original_value = self.raw_element.value
        self.raw_element.value = None
        element = self.TEST_CLASS(self.raw_element)
        self.assertIsNone(element.value)
        self.raw_element.value = ""
        element = self.TEST_CLASS(self.raw_element)
        self.assertIsNone(element.value)
        element = self.TEST_CLASS(self.raw_element)
        self.assertIsNone(element.value)
        self.raw_element.value = original_value

    def test_value_error(self):
        original_value = self.raw_element.value
        self.raw_element.value = "not_a_time"
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
        self.raw_element.value = False
        element = self.TEST_CLASS(self.raw_element)
        with self.assertRaises(TypeError):
            element.value
        self.raw_element.value = original_value

    def test_short_time(self):
        original_value = self.raw_element.value
        self.raw_element.value = "122156"
        element = self.TEST_CLASS(self.raw_element)
        self.assertIsInstance(element.value, datetime.time)
        self.raw_element.value = original_value
