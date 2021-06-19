"""
Definition of the :class:`OtherByteTestCase` class.
"""
from dicom_parser.data_elements.other_byte import OtherByte
from tests.test_data_element import DataElementTestCase


class OtherByteTestCase(DataElementTestCase):
    """
    Tests for the
    :class:`~dicom_parser.data_elements.other_byte.OtherByte`
    class.
    """

    TEST_CLASS = OtherByte
