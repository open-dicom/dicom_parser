"""
Definition of the :class:`OtherDoubleTestCase` class.
"""
from dicom_parser.data_elements.other_double import OtherDouble
from tests.test_data_element import DataElementTestCase


class OtherDoubleTestCase(DataElementTestCase):
    """
    Tests for the
    :class:`~dicom_parser.data_elements.other_double.OtherDouble`
    class.
    """

    TEST_CLASS = OtherDouble
