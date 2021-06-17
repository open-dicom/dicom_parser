"""
Definition of the :class:`UnlimitedTextTestCase` class.
"""
from dicom_parser.data_elements.unlimited_text import UnlimitedText
from tests.test_data_element import DataElementTestCase


class UnlimitedTextTestCase(DataElementTestCase):
    """
    Tests for the
    :class:`~dicom_parser.data_elements.unlimited_text.UnlimitedText`
    class.
    """

    TEST_CLASS = UnlimitedText
