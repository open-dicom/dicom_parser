"""
Definition of the :class:`Unsigned64bitVeryLongTestCase` class.
"""
from dicom_parser.data_elements.unsigned_64bit_very_long import (
    Unsigned64bitVeryLong,
)
from tests.test_data_element import DataElementTestCase


class Unsigned64bitVeryLongTestCase(DataElementTestCase):
    """
    Tests for the
    :class:`~dicom_parser.data_elements.unsigned_64bit_very_long.Unsigned64bitVeryLong`
    class.
    """

    TEST_CLASS = Unsigned64bitVeryLong
