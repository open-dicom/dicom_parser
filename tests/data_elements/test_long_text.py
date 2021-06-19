"""
Definition of the :class:`LongTextTestCase` class.
"""
from dicom_parser.data_elements.long_text import LongText
from tests.test_data_element import DataElementTestCase


class LongTextTestCase(DataElementTestCase):
    """
    Tests for the :class:`~dicom_parser.data_elements.long_text.LongText`
    class.
    """

    TEST_CLASS = LongText
