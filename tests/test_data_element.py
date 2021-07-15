"""
Definition of the :class:`DataElementTestCase` class.
"""
from typing import Tuple, Union
from unittest import TestCase

import numpy as np
import pydicom
from dicom_parser.data_element import DataElement
from dicom_parser.header import Header

from tests.data_elements.fixtures import VR_TO_VALUES
from tests.fixtures import TEST_IMAGE_PATH


class DataElementTestCase(TestCase):
    SKIP_MESSAGE: str = "No expected parsed values found for comparison."
    TEST_CLASS: DataElement = None
    TEST_IMAGE: str = TEST_IMAGE_PATH
    VALUES: dict = {}
    SAMPLE_KEY: str = ""

    raw_header: pydicom.dataset.FileDataset = None
    raw_element: pydicom.dataelem.DataElement = None

    @classmethod
    def setUpClass(cls):
        cls.raw_header = pydicom.dcmread(
            cls.TEST_IMAGE, stop_before_pixels=True
        )
        cls.header = Header(cls.TEST_IMAGE)

    def setUp(self):
        if self.SAMPLE_KEY:
            self.raw_element = self.raw_header.data_element(self.SAMPLE_KEY)

    def get_raw_element(
        self, key: Union[str, Tuple[int, int]]
    ) -> pydicom.dataelem.DataElement:
        return self.raw_header.data_element(key)

    def get_values(self) -> dict:
        vr = self.TEST_CLASS.VALUE_REPRESENTATION
        fixture = VR_TO_VALUES.get(vr, {})
        return self.VALUES if self.VALUES else fixture

    def test_parse_value(self):
        if self.TEST_CLASS is None:
            self.skipTest(self.SKIP_MESSAGE)
        values = self.get_values()
        for key, expected in values.items():
            raw = self.get_raw_element(key)
            value = self.TEST_CLASS(raw).value
            if isinstance(value, np.ndarray):
                self.assertTrue(np.array_equal(value, expected))
            else:
                self.assertEqual(value, expected)

    def test_repr(self):
        if not self.SAMPLE_KEY:
            self.skipTest("No sample key provided.")
        element = self.header.get_data_element(self.SAMPLE_KEY)
        self.assertEqual(repr(element), str(element))

    def test_is_public(self):
        if self.TEST_CLASS is None or self.SAMPLE_KEY == "":
            self.skipTest(self.SKIP_MESSAGE)
        element = self.TEST_CLASS(self.raw_element)
        self.assertTrue(element.is_public)

    def test_is_private(self):
        if self.TEST_CLASS is None or self.SAMPLE_KEY == "":
            self.skipTest(self.SKIP_MESSAGE)
        element = self.TEST_CLASS(self.raw_element)
        self.assertFalse(element.is_private)
