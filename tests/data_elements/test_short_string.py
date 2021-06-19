"""
Definition of the :class:`ShortStringTestCase` class.
"""
from dicom_parser.data_elements.short_string import ShortString
from tests.test_data_element import DataElementTestCase


class ShortStringTestCase(DataElementTestCase):
    """
    Tests for the :class:`~dicom_parser.data_elements.short_string.ShortString`
    class.
    """

    TEST_CLASS = ShortString
    SAMPLE_KEY = "StationName"
