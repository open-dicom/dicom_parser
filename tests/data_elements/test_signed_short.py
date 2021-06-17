"""
Definition of the :class:`SignedShortTestCase` class.
"""
from dicom_parser.data_elements.signed_short import SignedShort
from tests.test_data_element import DataElementTestCase


class SignedShortTestCase(DataElementTestCase):
    """
    Tests for the
    :class:`~dicom_parser.data_elements.signed_short.SignedShort`
    class.
    """

    TEST_CLASS = SignedShort
