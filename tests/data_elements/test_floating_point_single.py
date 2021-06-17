"""
Definition of the :class:`FloatingPointSingleTestCase` class.
"""
from dicom_parser.data_elements.floating_point_single import (
    FloatingPointSingle,
)
from tests.test_data_element import DataElementTestCase


class FloatingPointSingleTestCase(DataElementTestCase):
    """
    Tests for the
    :class:`~dicom_parser.data_elements.floating_point_single.FloatingPointSingle`
    class.
    """

    TEST_CLASS = FloatingPointSingle
