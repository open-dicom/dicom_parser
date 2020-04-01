from dicom_parser.image import Image
from dicom_parser.utils.sequence_detector.sequence_detector import SequenceDetector
from tests.fixtures import TEST_EP2D_IMAGE_PATH, TEST_IMAGE_PATH, TEST_RSFMRI_IMAGE_PATH
from unittest import TestCase


class SequenceDetectorCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sequence_detector = SequenceDetector()
        cls.mr_localizer_image = Image(TEST_IMAGE_PATH)
        cls.mr_ep2d_image = Image(TEST_EP2D_IMAGE_PATH)
        cls.mr_fmri_image = Image(TEST_RSFMRI_IMAGE_PATH)

    def test_detecting_mr_localizer(self):
        value = self.mr_localizer_image.header.detected_sequence
        expected = "Localizer"
        self.assertEqual(value, expected)

    def test_detecting_mr_ep2d(self):
        value = self.mr_ep2d_image.header.detected_sequence
        expected = "ep2d"
        self.assertEqual(value, expected)

    def test_detecting_mr_fmri(self):
        value = self.mr_fmri_image.header.detected_sequence
        expected = "fMRI"
        self.assertEqual(value, expected)

    def test_detecting_with_unknown_modality_raises_not_implemented_error(self):
        with self.assertRaises(NotImplementedError):
            self.sequence_detector.detect("AA", {"a": "a"})

    def test_detecting_with_bad_type_raises_type_error(self):
        bad_types = False, None, "string", 42, 4.20, b"bytes"
        for bad_type in bad_types:
            with self.assertRaises(TypeError):
                self.sequence_detector.check_definition(bad_type, {"a": "a"})

    def test_detecting_unknown_sequence_returns_none(self):
        self.assertIsNone(
            self.sequence_detector.detect("Magnetic Resonance", {"a": "a"})
        )
