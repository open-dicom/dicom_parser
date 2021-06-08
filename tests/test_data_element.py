from unittest import TestCase

from dicom_parser.header import Header

from tests.fixtures import (
    TEST_DATA_ELEMENT_BYTES_VALUE,
    TEST_DATA_ELEMENT_STRING,
    TEST_IMAGE_PATH,
    TEST_RSFMRI_IMAGE_PATH,
)


class HeaderTestCase(TestCase):
    TEST_ELEMENT_KEY: str = "PatientID"
    TEST_PRIVATE_BYTES_ELEMENT: tuple = "0051", "100f"
    TEST_SEQUENCE_ELEMENT: tuple = "0008", "1140"

    @classmethod
    def setUpClass(cls):
        cls.header = Header(TEST_IMAGE_PATH)
        cls.data_element = cls.header.get_data_element(cls.TEST_ELEMENT_KEY)
        cls.bytes_element = cls.header.get_data_element(
            cls.TEST_PRIVATE_BYTES_ELEMENT
        )
        cls.rsfmri_header = Header(TEST_RSFMRI_IMAGE_PATH)
        cls.sequence_element = cls.rsfmri_header.get_data_element(
            cls.TEST_SEQUENCE_ELEMENT
        )

    def test_str(self):
        value = str(self.data_element)
        expected = TEST_DATA_ELEMENT_STRING
        self.assertEqual(value, expected)

    def test_repr(self):
        value = repr(self.data_element)
        expected = TEST_DATA_ELEMENT_STRING
        self.assertEqual(value, expected)

    def test_parse_private_bytes_value(self):
        value = self.bytes_element.value
        expected = TEST_DATA_ELEMENT_BYTES_VALUE
        self.assertEqual(value, expected)

    def test_sequence_parse_value_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.sequence_element.parse_value("anything")
