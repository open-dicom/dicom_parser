"""
Definition of the :class:`DateTimeTestCase` class.
"""
from dicom_parser.data_elements.date_time import DateTime
from tests.test_data_element import DataElementTestCase


class DateTimeTestCase(DataElementTestCase):
    """
    Tests for the :class:`~dicom_parser.data_elements.date_time.DateTime`
    class.
    """

    TEST_CLASS = DateTime
