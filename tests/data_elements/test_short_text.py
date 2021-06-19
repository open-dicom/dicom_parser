"""
Definition of the :class:`ShortTextTestCase` class.
"""
from dicom_parser.data_elements.short_text import ShortText
from tests.test_data_element import DataElementTestCase


class ShortTextTestCase(DataElementTestCase):
    """
    Tests for the :class:`~dicom_parser.data_elements.short_text.ShortText`
    class.
    """

    TEST_CLASS = ShortText
    SAMPLE_KEY = "InstitutionAddress"
