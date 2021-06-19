"""
Definition of the :class:`SequenceOfItemsTestCase` class.
"""
from dicom_parser.data_elements.sequence_of_items import SequenceOfItems
from dicom_parser.header import Header
from tests.fixtures import TEST_SIEMENS_DWI_PATH
from tests.test_data_element import DataElementTestCase


class SequenceOfItemsTestCase(DataElementTestCase):
    """
    Tests for the
    :class:`~dicom_parser.data_elements.sequence_of_items.SequenceOfItems`
    class.
    """

    TEST_IMAGE = TEST_SIEMENS_DWI_PATH
    TEST_CLASS = SequenceOfItems

    TEST_SEQUENCE_KEY: str = "SourceImageSequence"

    def setUp(self):
        header = Header(self.TEST_IMAGE)
        self.sequence = header.get_data_element(self.TEST_SEQUENCE_KEY)

    def test_sequence_returns_list(self):
        value = self.sequence.value
        self.assertIsInstance(value, list)

    def test_sequence_returns_headers(self):
        header = self.sequence.value[0]
        self.assertIsInstance(header, Header)
        self.assertEqual(len(header.keys), 3)

    def test_parse_value_raises_notimplementederror(self):
        with self.assertRaises(NotImplementedError):
            self.sequence.parse_value(self.sequence.raw)
