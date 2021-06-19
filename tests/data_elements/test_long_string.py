"""
Definition of the :class:`LongStringTestCase` class.
"""
from dicom_parser.data_elements.long_string import LongString
from tests.test_data_element import DataElementTestCase


class LongStringTestCase(DataElementTestCase):
    """
    Tests for the :class:`~dicom_parser.data_elements.long_string.LongString`
    class.
    """

    TEST_CLASS = LongString
    SAMPLE_KEY = "InstitutionName"
