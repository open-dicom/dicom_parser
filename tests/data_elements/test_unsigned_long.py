"""
Definition of the :class:`UnsignedLongTestCase` class.
"""
from dicom_parser.data_elements.unsigned_long import UnsignedLong
from tests.test_data_element import DataElementTestCase


class UnsignedLongTestCase(DataElementTestCase):
    """
    Tests for the
    :class:`~dicom_parser.data_elements.unsigned_long.UnsignedLong`
    class.
    """

    TEST_CLASS = UnsignedLong
