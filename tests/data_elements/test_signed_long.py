"""
Definition of the :class:`SignedLongTestCase` class.
"""
from dicom_parser.data_elements.signed_long import SignedLong
from tests.test_data_element import DataElementTestCase


class SignedLongTestCase(DataElementTestCase):
    """
    Tests for the
    :class:`~dicom_parser.data_elements.signed_long.SignedLong`
    class.
    """

    TEST_CLASS = SignedLong
