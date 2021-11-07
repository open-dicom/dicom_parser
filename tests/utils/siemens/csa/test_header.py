from unittest import TestCase

import pydicom
from dicom_parser.utils.siemens.csa.header import CsaHeader
from dicom_parser.utils.siemens.private_tags import SIEMENS_PRIVATE_TAGS
from tests.fixtures import TEST_SIEMENS_DWI_PATH


TEST_DWI_HEADER_SIZE: int = 12964


class CsaHeaderTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        dcm = pydicom.dcmread(TEST_SIEMENS_DWI_PATH)
        tag = SIEMENS_PRIVATE_TAGS["CSAImageHeaderInfo"]
        cls.raw_csa = dcm.get(tag).value
        cls.csa = CsaHeader(cls.raw_csa)

    def test_init_stores_raw(self):
        self.assertEqual(self.csa.raw, self.raw_csa)

    def test_header_size(self):
        self.assertEqual(self.csa.header_size, TEST_DWI_HEADER_SIZE)

    def test_check_csa_type(self):
        value = self.csa.check_csa_type()
        expected = CsaHeader.CSA_TYPE_2
        self.assertEqual(value, expected)
