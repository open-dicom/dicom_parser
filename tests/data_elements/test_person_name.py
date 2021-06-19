"""
Definition of the :class:`PersonNameTestCase` class.
"""
from dicom_parser.data_elements.person_name import PersonName
from tests.test_data_element import DataElementTestCase


class PersonNameTestCase(DataElementTestCase):
    """
    Tests for the
    :class:`~dicom_parser.data_elements.person_name.PersonName`
    class.
    """

    TEST_CLASS = PersonName
    SAMPLE_KEY = "PatientName"
