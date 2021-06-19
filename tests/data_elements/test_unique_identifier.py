"""
Definition of the :class:`UniqueIdentifierTestCase` class.
"""
from dicom_parser.data_elements.unique_identifier import UniqueIdentifier
from tests.test_data_element import DataElementTestCase


class UniqueIdentifierTestCase(DataElementTestCase):
    """
    Tests for the
    :class:`~dicom_parser.data_elements.unique_identifier.UniqueIdentifier`
    class.
    """

    TEST_CLASS = UniqueIdentifier
    SAMPLE_KEY = "SeriesInstanceUID"
