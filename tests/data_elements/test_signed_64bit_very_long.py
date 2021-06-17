"""
Definition of the :class:`Signed64bitVeryLongTestCase` class.
"""
from dicom_parser.data_elements.signed_64bit_very_long import (
    Signed64bitVeryLong,
)
from tests.test_data_element import DataElementTestCase


class Signed64bitVeryLongTestCase(DataElementTestCase):
    """
    Tests for the
    :class:`~dicom_parser.data_elements.signed_64bit_very_long.Signed64bitVeryLong`
    class.
    """

    TEST_CLASS = Signed64bitVeryLong
