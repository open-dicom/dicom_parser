"""
Definition of the :class:`UnsignedShortTestCase` class.
"""
from dicom_parser.data_elements.unsigned_short import UnsignedShort
from tests.test_data_element import DataElementTestCase


class UnsignedShortTestCase(DataElementTestCase):
    """
    Tests for the
    :class:`~dicom_parser.data_elements.unsigned_short.UnsignedShort`
    class.
    """

    TEST_CLASS = UnsignedShort
    SAMPLE_KEY = "BitsStored"
