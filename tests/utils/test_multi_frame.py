"""
Tests for the :class:`dicom_parser.utils.multi_frame.multi_frame.MultiFrame`
class.

TODO
----
* Find multi-stack multi-frame image to test NotImplementedError or implement
  parsing.
* Find Phillips image with a derived appendix to test exclusion in frames info.
* Find 3D multi-frame to test.
* Find multi-frame with rescaling information included in transformations or
  create values.
"""
from unittest import TestCase

import numpy as np
from dicom_parser.image import Image
from dicom_parser.utils.exceptions import DicomParsingError
from dicom_parser.utils.multi_frame import MultiFrame
from tests.fixtures import TEST_IMAGE_PATH, TEST_MULTIFRAME


class MultiFrameTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.image = Image(TEST_MULTIFRAME)
        cls.multi_frame = MultiFrame(cls.image._data, cls.image.header)

    def test_image_shape(self):
        value = self.multi_frame.image_shape
        expected = (512, 512, 56, 2)
        self.assertTupleEqual(value, expected)

    def test_image_position(self):
        value = self.multi_frame.image_position
        expected = np.array([-163.2, 93.3, 195.8])
        self.assertTrue(np.array_equal(value, expected))

    def test_voxel_sizes(self):
        value = self.multi_frame.voxel_sizes
        expected = (0.625, 0.625, 3.0)
        self.assertTupleEqual(value, expected)

    def test_image_orientation_patient(self):
        value = self.multi_frame.image_orientation_patient
        expected = np.array([[1.0, 0.0], [0.0, 0.0], [0.0, -1.0]])
        self.assertTrue(np.array_equal(value, expected))

    def test_get_data(self):
        value = self.multi_frame.get_data()
        scaled = self.image.data  # Scaling is meaningless in our test
        expected = np.load(TEST_MULTIFRAME.replace("dcm", "npy"))
        self.assertTrue(np.array_equal(value, expected))
        self.assertTrue(np.array_equal(scaled, expected))

    def test_bad_n_frames_raises_error(self):
        original_value = self.image.header["NumberOfFrames"]
        self.image.header.raw["NumberOfFrames"].value = 100
        bad_mf = MultiFrame(self.image._data, self.image.header)
        with self.assertRaises(DicomParsingError):
            bad_mf.get_data()
        self.image.header.raw["NumberOfFrames"].value = original_value

    def test_image_shape_with_missing_rows(self):
        original_value = self.image.header["Rows"]
        self.image.header.raw["Rows"].value = None
        bad_mf = MultiFrame(self.image._data, self.image.header)
        self.assertIsNone(bad_mf.image_shape)
        self.image.header.raw["Rows"].value = original_value

    def test_get_data_with_missing_rows_raises_error(self):
        original_value = self.image.header["Rows"]
        self.image.header.raw["Rows"].value = None
        bad_mf = MultiFrame(self.image._data, self.image.header)
        with self.assertRaises(DicomParsingError):
            bad_mf.get_data()
        self.image.header.raw["Rows"].value = original_value

    def test_image_shape_with_missing_columns(self):
        original_value = self.image.header["Columns"]
        self.image.header.raw["Columns"].value = None
        bad_mf = MultiFrame(self.image._data, self.image.header)
        self.assertIsNone(bad_mf.image_shape)
        self.image.header.raw["Columns"].value = original_value

    def test_get_data_with_missing_columns_raises_error(self):
        original_value = self.image.header["Columns"]
        self.image.header.raw["Columns"].value = None
        bad_mf = MultiFrame(self.image._data, self.image.header)
        with self.assertRaises(DicomParsingError):
            bad_mf.get_data()
        self.image.header.raw["Columns"].value = original_value

    def test_get_scaling_parameters(self):
        value = self.multi_frame.get_scaling_parameters()
        expected = (1, 0)
        self.assertTupleEqual(value, expected)

    def test_missing_pixel_measures_raises_error(self):
        # PixelMeasuresSequence only exists within the shared sequence in the
        # sample image, so the first "per frame" sequence is used to check the
        # exception is raised.
        with self.assertRaises(DicomParsingError):
            self.multi_frame.sample_sequence.get_pixel_measures()

    def test_missing_pixel_measures_fallback(self):
        # Tests to cover cases where the shared group doesn't provide the
        # information and the sample per frame should be checked.
        mf = MultiFrame(self.image._data, self.image.header)
        shared_group = mf.shared_functional_groups
        original_value = shared_group.frame_header.raw[
            "PixelMeasuresSequence"
        ].value
        shared_group.frame_header.raw["PixelMeasuresSequence"].value = None
        with self.assertRaises(DicomParsingError):
            mf.get_pixel_measures()
        shared_group.frame_header.raw[
            "PixelMeasuresSequence"
        ].value = original_value

    def test_missing_index_without_content_group_raises_error(self):
        # Frame index only exists within the "per frame" sequence in the sample
        # image, so the first shared sequence is used to check the exception is
        # raised.
        with self.assertRaises(DicomParsingError):
            self.multi_frame.shared_functional_groups.get_index()

    def test_missing_index_with_content_group_raises_error(self):
        sequence = self.multi_frame.sample_sequence
        del sequence.content_sequence.raw["DimensionIndexValues"]
        with self.assertRaises(DicomParsingError):
            sequence.get_index()

    def test_missing_stack_id_without_content_group(self):
        # Frame index only exists within the "per frame" sequence in the sample
        # image, so the first shared sequence is used to check the exception is
        # raised.
        with self.assertRaises(DicomParsingError):
            self.multi_frame.shared_functional_groups.get_stack_id()

    def test_missing_stack_id_with_content_group_raises_error(self):
        sequence = self.multi_frame.sample_sequence
        del sequence.content_sequence.raw["StackID"]
        with self.assertRaises(DicomParsingError):
            sequence.get_stack_id()

    def test_bad_header_raises_error(self):
        image = Image(TEST_IMAGE_PATH)
        with self.assertRaises(DicomParsingError):
            MultiFrame(image._data, image.header)

    def test_empty_shared_sequence_raises_error(self):
        image = Image(TEST_MULTIFRAME)
        key = MultiFrame.SHARED_GROUPS_KEY
        image.header.raw[key].value = []
        mf = MultiFrame(image._data, image.header)
        with self.assertRaises(DicomParsingError):
            mf.get_functional_groups(shared=True)

    def test_missing_dimension_index_pointers_raises_error(self):
        mf = MultiFrame(self.image._data, self.image.header)
        del mf.header.raw["DimensionIndexSequence"]
        with self.assertRaises(DicomParsingError):
            mf.get_dimension_index_pointers()

    def test_missing_diffusion_sequence_raises_error(self):
        with self.assertRaises(DicomParsingError):
            self.multi_frame.sample_sequence.get_diffusion_sequence()

    def test_missing_diffusion_directionality_raises_error(self):
        with self.assertRaises(DicomParsingError):
            self.multi_frame.sample_sequence.get_diffusion_directionality()

    def test_missing_shared_plane_orientation_raises_error(self):
        mf = MultiFrame(self.image._data, self.image.header)
        shared_group = mf.shared_functional_groups
        del shared_group.frame_header.raw["PlaneOrientationSequence"]
        with self.assertRaises(DicomParsingError):
            mf.get_image_orientation_patient()

    def test_missing_image_orientation_patient_raises_error(self):
        mf = MultiFrame(self.image._data, self.image.header)
        shared_group = mf.shared_functional_groups
        del shared_group.frame_header["PlaneOrientationSequence"][0].raw[
            "ImageOrientationPatient"
        ]
        with self.assertRaises(DicomParsingError):
            mf.get_image_orientation_patient()

    def test_missing_pixel_spacing_raises_error(self):
        mf = MultiFrame(self.image._data, self.image.header)
        shared_group = mf.shared_functional_groups
        original_value = shared_group.frame_header["PixelMeasuresSequence"][
            0
        ].raw["PixelSpacing"]
        del shared_group.frame_header["PixelMeasuresSequence"][0].raw[
            "PixelSpacing"
        ]
        with self.assertRaises(DicomParsingError):
            mf.get_voxel_sizes()
        shared_group.frame_header["PixelMeasuresSequence"][0].raw[
            "PixelSpacing"
        ] = original_value

    def test_missing_slice_thickness_raises_error(self):
        mf = MultiFrame(self.image._data, self.image.header)
        shared_group = mf.shared_functional_groups
        original_value = shared_group.frame_header["PixelMeasuresSequence"][
            0
        ].raw["SliceThickness"]
        del shared_group.frame_header["PixelMeasuresSequence"][0].raw[
            "SliceThickness"
        ]
        with self.assertRaises(DicomParsingError):
            mf.get_voxel_sizes()
        shared_group.frame_header["PixelMeasuresSequence"][0].raw[
            "SliceThickness"
        ] = original_value

    def test_missing_image_position_patient_raises_error(self):
        mf = MultiFrame(self.image._data, self.image.header)
        header = mf.sample_sequence.frame_header
        original_value = header["PlanePositionSequence"][0].raw[
            "ImagePositionPatient"
        ]
        del header["PlanePositionSequence"][0].raw["ImagePositionPatient"]
        with self.assertRaises(DicomParsingError):
            mf.get_image_position()
        header["PlanePositionSequence"][0].raw[
            "ImagePositionPatient"
        ] = original_value

    def test_property_caching(self):
        self.assertIs(
            self.multi_frame.frame_functional_groups,
            self.multi_frame._frame_functional_groups,
        )
        self.assertIs(
            self.multi_frame.shared_functional_groups,
            self.multi_frame._shared_functional_groups,
        )
        self.assertIs(
            self.multi_frame.frame_indices, self.multi_frame._frame_indices
        )
        self.assertIs(self.multi_frame.stack_ids, self.multi_frame._stack_ids)
        self.assertIs(self.multi_frame.stack_ids, self.multi_frame._stack_ids)
        self.assertIs(
            self.multi_frame.image_orientation_patient,
            self.multi_frame._image_orientation_patient,
        )
        self.assertIs(
            self.multi_frame.image_position, self.multi_frame._image_position
        )
        self.assertIs(
            self.multi_frame.image_shape, self.multi_frame._image_shape
        )
        self.assertIs(self.multi_frame.n_frames, self.multi_frame._n_frames)
        self.assertIs(
            self.multi_frame.frame_indices, self.multi_frame._frame_indices
        )
        self.assertIs(
            self.multi_frame.voxel_sizes, self.multi_frame._voxel_sizes
        )
        self.assertIs(
            self.multi_frame.dimension_index_pointers,
            self.multi_frame._dimension_index_pointers,
        )
