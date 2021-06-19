"""
Definition of the :class:`ApplicationEntityTestCase` class.
"""
from dicom_parser.data_elements.application_entity import ApplicationEntity
from tests.test_data_element import DataElementTestCase


class ApplicationEntityTestCase(DataElementTestCase):
    """
    Tests for the
    :class:`~dicom_parser.data_elements.application_entity.ApplicationEntity`
    class.
    """

    TEST_CLASS = ApplicationEntity
