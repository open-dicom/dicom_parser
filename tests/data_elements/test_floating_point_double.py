"""
Definition of the :class:`FloatingPointDoubleTestCase` class.
"""
from dicom_parser.data_elements.floating_point_double import (
    FloatingPointDouble,
)
from tests.test_data_element import DataElementTestCase


class FloatingPointDoubleTestCase(DataElementTestCase):
    """
    Tests for the
    :class:`~dicom_parser.data_elements.floating_point_double.FloatingPointDouble`
    class.
    """

    TEST_CLASS = FloatingPointDouble
