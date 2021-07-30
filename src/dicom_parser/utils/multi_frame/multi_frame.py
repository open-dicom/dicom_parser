"""
Definition of the :class:`MultiFrame` class.
"""
from typing import List, Tuple

import numpy as np
from dicom_parser.header import Header
from dicom_parser.utils.exceptions import DicomParsingError
from dicom_parser.utils.multi_frame import messages
from dicom_parser.utils.multi_frame.functional_groups import FunctionalGroups
from pydicom.datadict import tag_for_keyword
from pydicom.tag import BaseTag


class MultiFrame:
    """
    Handles Enhanced MR Storage SOP Class encoded data.

    References
    ----------
    * NiBabel's `original implementation`_.

    .. _original implementation:
       https://github.com/nipy/nibabel/blob/62aea04248e70d7c4529954ca41685d7f75a0b1e/nibabel/nicom/dicomwrappers.py#L422
    """

    #: Keeps a cached copy of the per frame functional groups header
    #: information.
    _frame_functional_groups: List[Header] = None

    #: Keeps a cached copy of the calculated image orientation (patient) header
    #: information.
    _image_orientation_patient: np.ndarray = None

    #: Keeps a cached copy of the image position header information.
    _image_position: np.ndarray = None

    #: Keeps a cached copy of the image shape header information.
    _image_shape: tuple = None

    #: Keeps a cached copy of the shared functional groups header information.
    _shared_functional_groups: List[Header] = None

    #: Keeps a cached copy of the number of frames.
    _n_frames: tuple = None

    #: Keeps a cached copy of the frame indices.
    _frame_indices: np.ndarray = None

    #: Keeps a cached copy of the frame stack IDs.
    _stack_ids: Tuple[str] = None

    #: Keeps a cached copy of the voxel sizes.
    _voxel_sizes: Tuple[float, float, float] = None

    #: Keeps a chached copy of the dimension index pointers.
    _dimension_index_pointers: List[BaseTag] = None

    #: Stack ID tag (in integer representation), used to remove any dimension
    #: indices pointing to it.
    STACK_ID_TAG: int = tag_for_keyword("StackID")

    #: Diffusion B-value tag (in integer representation), used to evaluate the
    #: inclusion of a derived volume.
    DERIVED_VOLUME_TAG: int = tag_for_keyword("DiffusionBValue")

    #: Key to use for reading the per frame functional groups sequence.
    PER_FRAME_GROUPS_KEY: str = "PerFrameFunctionalGroupsSequence"

    #: Key to use for reading the shared functional groups sequence.
    SHARED_GROUPS_KEY: str = "SharedFunctionalGroupsSequence"

    def __init__(self, pixel_array: np.ndarray, header: Header):
        """
        Initializes a new :class:`MultiFrame` instance.

        Parameters
        ----------
        pixel_array : np.ndarray
            Raw pixel array
        header : Header
            Image header information
        """
        self.pixel_array: np.ndarray = pixel_array
        self.header: Header = header
        self.sample_sequence = self.frame_functional_groups[0]
        self.has_derived_appendix: bool = self.sample_sequence.appendix_flag
        self.validate_single_stack()

    def validate_single_stack(self):
        """
        Validate single stack image.

        Raises
        ------
        NotImplementedError
            Multi stack multi-frame images are not yet supported
        """
        n_stack_ids = len(set(self.stack_ids))
        if n_stack_ids > 1:
            message = messages.MULTIPLE_STACK_IDS
            raise NotImplementedError(message)

    def get_functional_groups(self, shared: bool = False) -> List[Header]:
        """
        Reads functional groups information from the header.

        Parameters
        ----------
        shared : bool
            Whether to read the shared (rather than per frame) sequence,
            default is False

        See Also
        --------
        * :func:`frame_functional_groups`

        Returns
        -------
        List[Header]
            Frame header information
        """
        key = self.SHARED_GROUPS_KEY if shared else self.PER_FRAME_GROUPS_KEY
        try:
            sequence = self.header[key]
        except KeyError:
            sequence_type = "shared" if shared else "per frame"
            message = messages.MISSING_FUNCTIONAL_GROUPS.format(
                sequence_type=sequence_type
            )
            raise DicomParsingError(message)
        if shared:
            try:
                return FunctionalGroups(sequence[0])
            except IndexError:
                message = messages.EMPTY_SHARED_FUNCTIONAL_GROUPS
                raise DicomParsingError(message)
        groups = [FunctionalGroups(frame_header) for frame_header in sequence]
        return [group for group in groups if not group.is_appendix]

    def get_n_frames(self) -> int:
        """
        Returns the number of frames encoded in this multi-frame data.

        See Also
        --------
        * :func:`n_frames`

        Returns
        -------
        int
            Number of frames

        Raises
        ------
        DicomParsingError
            Ambiguous number of frames
        """
        n_frame_info = len(self.frame_functional_groups)
        if self.has_derived_appendix:
            return n_frame_info
        header_n_frames = self.header.get("NumberOfFrames")
        if n_frame_info != header_n_frames:
            message = messages.AMBIGUOUS_N_FRAMES
            raise DicomParsingError(message)
        return header_n_frames

    def remove_derived_appendix(self, frames: List[Header]) -> List[Header]:
        """
        Removes derived frames that may be appended to the data.

        Parameters
        ----------
        frames : List[Header]
            All encoded frames

        Returns
        -------
        List[Header]
            Frames without derived data
        """
        return [frame for frame in frames if self.check_frame_inclusion(frame)]

    def get_dimension_index_pointers(self) -> Tuple[BaseTag]:
        """
        Returns the dimensions index pointers from the header.

        See Also
        --------
        * :func:`dimension_index_pointers`

        Returns
        -------
        Tuple[BaseTag]
            Dimension index pointers

        Raises
        ------
        DicomParsingError
            Failed to read dimension index pointers
        """
        try:
            return tuple(
                dimension["DimensionIndexPointer"]
                for dimension in self.header["DimensionIndexSequence"]
            )
        except (KeyError, TypeError) as e:
            message = messages.MISSING_DIMENSION_INDEX_POINTERS.format(
                exception=e
            )
            raise DicomParsingError(message)

    def get_frame_indices(self) -> np.ndarray:
        """
        Returns an array of frame indices.

        See Also
        --------
        * :func:`frame_indices`

        Returns
        -------
        np.ndarray
            Frame indices
        """
        indices = [group.get_index() for group in self.frame_functional_groups]
        pointers = self.dimension_index_pointers
        # Remove dimension indices refering to stack IDs.
        if self.STACK_ID_TAG in pointers:
            index = pointers.index(self.STACK_ID_TAG)
            indices = np.delete(indices, index, axis=1)
            pointers = tuple(
                tag for tag in pointers if tag != self.STACK_ID_TAG
            )
        # Remove dimension indices refering to derived volumes.
        if self.has_derived_appendix:
            if self.DERIVED_VOLUME_TAG not in pointers:
                message = messages.MISSING_DERIVED_INDICES
                raise DicomParsingError(message)
            index = pointers.index(self.DERIVED_VOLUME_TAG)
            indices = np.delete(indices, index, axis=1)
        return np.array(indices)

    def get_stack_ids(self) -> Tuple[str]:
        """
        Returns a tuple of stack IDs by frame.

        Returns
        -------
        Tuple[str]
            Stack IDs by frame
        """
        return tuple(
            group.get_stack_id() for group in self.frame_functional_groups
        )

    def validate_high_dim_shape(self, shape: tuple) -> None:
        """
        Validates the calculated image shape matches the number of frames in
        the dataset.

        See Also
        --------
        * :func:`calculate_high_dim_shape`

        Parameters
        ----------
        shape : tuple
            Calculated image shape

        Raises
        ------
        DicomParsingError
            Header/data information mismatch
        """
        n_volumes = np.prod(shape[3:])
        n_frames_expected = n_volumes * shape[2]
        if self.n_frames != n_frames_expected:
            message = messages.SHAPE_MISMATCH.format(
                n_volumes=n_volumes,
                n_calculated=n_frames_expected,
                n_frames=self.n_frames,
            )
            raise DicomParsingError(message)

    def calculate_high_dim_shape(self, rows: int, columns: int) -> Tuple[int]:
        """
        Calculates the image shape for high dimensionality (>3D) data.

        See Also
        --------
        * :func:`validate_high_dim_shape`

        Parameters
        ----------
        rows : int
            Number of rows in a frame
        columns : int
            Number of columns in a frame

        Returns
        -------
        Tuple[int]
            Image shape

        Raises
        ------
        DicomParsingError
            Failed to parse image shape
        """
        n_unique = [len(np.unique(row)) for row in self.frame_indices.T]
        shape = (rows, columns) + tuple(n_unique)
        self.validate_high_dim_shape(shape)
        return shape

    def get_image_shape(self) -> tuple:
        """
        Returns the calculated shape of the image.

        See Also
        --------
        * :func:`image_shape`

        Returns
        -------
        tuple
            Image shape
        """
        rows = self.header.get("Rows")
        columns = self.header.get("Columns")
        if rows is None or columns is None:
            return None
        # Account for rows and columns in the total number of dimensions.
        n_dim = self.frame_indices.shape[1] + 2
        # 3D volume.
        if n_dim < 4:
            return rows, columns, self.n_frames
        # 4D data.
        return self.calculate_high_dim_shape(rows, columns)

    def get_image_orientation_patient(self) -> np.ndarray:
        """
        Returns the image position and orientation.

        References
        ----------
        * https://dicom.innolitics.com/ciods/mr-image/image-plane/00200037

        See Also
        --------
        * :func:`image_orientation_patient`

        Returns
        -------
        np.array
            Parsed image orientation (patient) attribute information
        """
        try:
            plane_orientation = (
                self.shared_functional_groups.get_plane_orientation()
            )
        except DicomParsingError:
            plane_orientation = self.sample_sequence.get_plane_orientation()
        try:
            iop = plane_orientation["ImageOrientationPatient"]
        except KeyError:
            raise DicomParsingError(messages.MISSING_PLANE_ORIENTATION)
        else:
            iop = np.array(list(map(float, iop)))
            return np.array(iop).reshape(2, 3).T

    def get_pixel_measures(self) -> Header:
        """
        Returns the pixel measures sequence.

        Returns
        -------
        Header
            Pixel measures sequence

        Raises
        ------
        DicomParsingError
            Pixel measures sequence could not be read
        """
        try:
            return self.shared_functional_groups.get_pixel_measures()
        except DicomParsingError:
            return self.sample_sequence.get_pixel_measures()

    def get_voxel_sizes(self) -> Tuple[float, float, float]:
        """
        Returns the voxel sizes of the image.

        See Also
        --------
        * :func:`voxel_sizes`

        Returns
        -------
        Tuple[float, float, float]
            Voxel sizes

        Raises
        ------
        DicomParsingError
            Voxel sizes could not be determines
        """
        pixel_measures = self.get_pixel_measures()
        try:
            pixel_spacing = pixel_measures["PixelSpacing"]
        except KeyError:
            message = messages.MISSING_PIXEL_SPACING
            raise DicomParsingError(message)
        try:
            slice_thickness = pixel_measures["SliceThickness"]
        except KeyError:
            try:
                slice_thickness = self.header["SpacingBetweenSlices"]
            except KeyError:
                message = messages.MISSING_SLICE_THICKNESS
                raise DicomParsingError(message)
        sizes = list(pixel_spacing) + [slice_thickness]
        return tuple(map(float, sizes))

    def get_image_position(self) -> np.ndarray:
        """
        Returns the image position.

        See Also
        --------
        * :func:`image_position`

        Returns
        -------
        np.ndarray
            Image position

        Raises
        ------
        DicomParsingError
            Image position could not be determined
        """
        try:
            plane_position = self.shared_functional_groups.get_plane_position()
        except DicomParsingError:
            plane_position = self.sample_sequence.get_plane_position()
        try:
            ipp = plane_position["ImagePositionPatient"]
        except KeyError:
            raise DicomParsingError(messages.MISSING_IMAGE_POSITION)
        else:
            return np.array(list(map(float, ipp)))

    def get_pixel_value_transformations(self) -> Header:
        """
        Returns any pixel value transformations included in the first frame's
        functional groups sequence, or `None`.

        See Also
        --------
        * :func:`get_scaling_parameters`

        Returns
        -------
        Header
            Pixel value transformations
        """
        try:
            return self.sample_sequence.get_pixel_value_transformations()
        except DicomParsingError:
            pass

    def get_scaling_parameters(self) -> np.ndarray:
        """
        Returns the scaling parameters (slope and intercept) for the pixel
        array.

        See Also
        --------
        * :func:`get_pixel_value_transformations`

        Returns
        -------
        np.ndarray
            Scaled pixel array
        """
        transformation = self.get_pixel_value_transformations()
        try:
            slope = float(transformation[0]["RescaleSlope"])
            intercept = float(transformation[0]["RescaleIntercept"])
        except (KeyError, IndexError, TypeError):
            slope = self.header.get("RescaleSlope", 1)
            intercept = self.header.get("RescaleIntercept", 0)
        return (slope, intercept)

    def get_data(self) -> np.ndarray:
        """
        Returns the parsed multi-frame image pixel array.

        Returns
        -------
        np.ndarray
            Pixel array

        Raises
        ------
        DicomParsingError
            Failed to parse multi-frame pixel array
        """
        if self.image_shape is None:
            message = messages.MISSING_IMAGE_SHAPE
            raise DicomParsingError(message)
        # Roll frames axis to last.
        data = self.pixel_array.transpose((1, 2, 0))
        # Sort frames with first index changing fastest, last slowest.
        sorted_indices = np.lexsort(self.frame_indices.T)
        data = data[..., sorted_indices]
        return data.reshape(self.image_shape, order="F")

    @property
    def frame_functional_groups(self) -> int:
        """
        Keeps a cached reference to per frame header information.

        See Also
        --------
        * :func:`get_frame_functional_groups`

        Returns
        -------
        List[Header]
            Per frame header information
        """
        if self._frame_functional_groups is None:
            self._frame_functional_groups = self.get_functional_groups(
                shared=False
            )
        return self._frame_functional_groups

    @property
    def shared_functional_groups(self) -> int:
        """
        Keeps a cached reference to shared header information.

        See Also
        --------
        * :func:`get_functional_groups`

        Returns
        -------
        List[Header]
            Shared header information
        """
        if self._shared_functional_groups is None:
            self._shared_functional_groups = self.get_functional_groups(
                shared=True
            )
        return self._shared_functional_groups

    @property
    def n_frames(self) -> int:
        """
        Returns the number of frames encoded in this multi-frame data.

        See Also
        --------
        * :func:`get_n_frames`

        Returns
        -------
        int
            Number of frames
        """
        if self._n_frames is None:
            self._n_frames = self.get_n_frames()
        return self._n_frames

    @property
    def frame_indices(self) -> np.ndarray:
        """
        Returns an array of frame indices.

        See Also
        --------
        * :func:`get_frame_indices`

        Returns
        -------
        np.ndarray
            Frame indices
        """
        if self._frame_indices is None:
            self._frame_indices = self.get_frame_indices()
        return self._frame_indices

    @property
    def stack_ids(self) -> Tuple[str]:
        """
        Returns a tuple of stack IDs by frame.

        See Also
        --------
        * :func: `get_stack_ids`

        Returns
        -------
        Tuple[str]
            Stack ID by frame
        """
        if self._stack_ids is None:
            self._stack_ids = self.get_stack_ids()
        return self._stack_ids

    @property
    def dimension_index_pointers(self) -> List[BaseTag]:
        """
        Returns the dimensions index pointers from the header.

        See Also
        --------
        * :func:`get_dimension_index_pointers`

        Returns
        -------
        List[BaseTag]
            Dimension index pointers

        Raises
        ------
        DicomParsingError
            Failed to read dimension index pointers
        """
        if self._dimension_index_pointers is None:
            self._dimension_index_pointers = (
                self.get_dimension_index_pointers()
            )
        return self._dimension_index_pointers

    @property
    def image_orientation_patient(self) -> np.ndarray:
        """
        Returns the image position and orientation.

        See Also
        --------
        * :func:`get_image_orientation_patient`

        Returns
        -------
        np.array
            Parsed image orientation (patient) attribute information
        """
        if self._image_orientation_patient is None:
            self._image_orientation_patient = (
                self.get_image_orientation_patient()
            )
        return self._image_orientation_patient

    @property
    def voxel_sizes(self) -> Tuple[float, float, float]:
        """
        Returns the voxel sizes of the image.

        See Also
        --------
        * :func:`get_voxel_sizes`

        Returns
        -------
        Tuple[float, float, float]
            Voxel sizes

        Raises
        ------
        DicomParsingError
            Voxel sizes could not be determines
        """
        if self._voxel_sizes is None:
            self._voxel_sizes = self.get_voxel_sizes()
        return self._voxel_sizes

    @property
    def image_position(self) -> np.ndarray:
        """
        Returns the image position.

        See Also
        --------
        * :func:`get_image_position`

        Returns
        -------
        np.ndarray
            Image position

        Raises
        ------
        DicomParsingError
            Image position could not be determined
        """
        if self._image_position is None:
            self._image_position = self.get_image_position()
        return self._image_position

    @property
    def image_shape(self) -> tuple:
        """
        Returns the calculated shape of the image.

        See Also
        --------
        * :func:`get_image_shape`

        Returns
        -------
        tuple
            Image shape
        """
        if self._image_shape is None:
            self._image_shape = self.get_image_shape()
        return self._image_shape
