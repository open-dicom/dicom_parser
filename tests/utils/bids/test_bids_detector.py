from unittest import TestCase

from dicom_parser.header import Header
from tests.fixtures import TEST_MPRAGE_IMAGE_PATH
from tests.utils.bids.fixtures import BIDS_PATH


class BidsDetectorTestCase(TestCase):
    """
    Tests for the
    :class:`~dicom_parser.utils.bids.bids_detector.BidsDetector` class.
    """

    @classmethod
    def setUpClass(cls):
        cls.mprage_header = Header(TEST_MPRAGE_IMAGE_PATH)

    def test_build_corrected_mprage_bids_path(self):
        value = self.mprage_header.build_bids_path()
        expected = BIDS_PATH["mprage"]["corrected"]
        self.assertEqual(value, expected)
