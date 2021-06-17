"""
Definition of the :class:`OtherLongTestCase` class.
"""
from dicom_parser.data_elements.other_long import OtherLong
from tests.test_data_element import DataElementTestCase


class OtherLongTestCase(DataElementTestCase):
    """
    Tests for the :class:`~dicom_parser.data_elements.other_long.OtherLong`
    class.
    """

    TEST_CLASS = OtherLong
