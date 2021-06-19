"""
Definition of the :class:`Other64bitVeryLongTestCase` class.
"""
from dicom_parser.data_elements.other_64bit_very_long import Other64bitVeryLong
from tests.test_data_element import DataElementTestCase


class Other64bitVeryLongTestCase(DataElementTestCase):
    """
    Tests for the
    :class:`~dicom_parser.data_elements.other_64bit_very_long.Other64bitVeryLong`
    class.
    """

    TEST_CLASS = Other64bitVeryLong
