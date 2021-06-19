"""
Definition of the :class:`CodeStringTestCase` class.
"""
from dicom_parser.data_elements.code_string import CodeString
from tests.fixtures import TEST_SIEMENS_DWI_PATH
from tests.test_data_element import DataElementTestCase


class CodeStringTestCase(DataElementTestCase):
    """
    Tests for the :class:`~dicom_parser.data_elements.code_string.CodeString`
    class.
    """

    TEST_IMAGE = TEST_SIEMENS_DWI_PATH
    TEST_CLASS = CodeString
    SAMPLE_KEY = "SequenceVariant"
