"""
Definition of the :class:`OtherWordTestCase` class.
"""
from dicom_parser.data_elements.other_word import OtherWord
from tests.data_elements.fixtures import TEST_OW_ELEMENT, TEST_OW_EXPECTED
from tests.test_data_element import DataElementTestCase


class OtherWordTestCase(DataElementTestCase):
    """
    Tests for the :class:`~dicom_parser.data_elements.other_word.OtherWord`
    class.
    """

    TEST_CLASS = OtherWord

    def test_parse_value(self):
        self.raw_header.add_new(*TEST_OW_ELEMENT)
        raw = self.raw_header[0x72, 0x69]
        element = self.TEST_CLASS(raw)
        self.assertEqual(element.value, TEST_OW_EXPECTED)
