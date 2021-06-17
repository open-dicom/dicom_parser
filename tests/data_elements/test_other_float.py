"""
Definition of the :class:`OtherFloatTestCase` class.
"""
from dicom_parser.data_elements.other_float import OtherFloat
from tests.test_data_element import DataElementTestCase


class OtherFloatTestCase(DataElementTestCase):
    """
    Tests for the
    :class:`~dicom_parser.data_elements.other_float.OtherFloat`
    class.
    """

    TEST_CLASS = OtherFloat
