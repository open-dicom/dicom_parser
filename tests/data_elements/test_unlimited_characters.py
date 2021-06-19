"""
Definition of the :class:`UnlimitedCharactersTestCase` class.
"""
from dicom_parser.data_elements.unlimited_characters import UnlimitedCharacters
from tests.test_data_element import DataElementTestCase


class UnlimitedCharactersTestCase(DataElementTestCase):
    """
    Tests for the
    :class:`~dicom_parser.data_elements.unlimited_characters.UnlimitedCharacters`
    class.
    """

    TEST_CLASS = UnlimitedCharacters
