"""
Definition of the :class:`MultiFrame` class.
"""
from typing import List, Tuple

import numpy as np
from dicom_parser.header import Header
from dicom_parser.utils.exceptions import DicomParsingError
from dicom_parser.utils.multi_frame.messages import (
    AMBIGUOUS_N_FRAMES,
    INVALID_DIFFUSION_SEQUENCE,
    MISSING_DERIVED_INDICES,
    MISSING_DIMENSION_INDEX_POINTERS,
    MISSING_FRAME_INDEX,
    MISSING_FUNCTIONAL_GROUPS,
    MISSING_STACK_ID,
    MULTIPLE_STACK_IDS,
    SHAPE_MISMATCH,
)
from pydicom.datadict import tag_for_keyword
from pydicom.tag import BaseTag

#: Phillips derived data appendix data element tag.
PHILLIPS_APPENDIX_FLAG: Tuple[float, float] = (0x18, 0x9117)


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

    #: Keeps a cached copy of the shared functional groups header information.
    _shared_functional_groups: List[Header] = None

    #: Keeps a cached copy of the calculated image shape.
    _shape: tuple = None

    #: Keeps a cached copy of the number of frames.
    _n_frames: tuple = None

    #: Keeps a cached copy of the frame indices.
    _frame_indices: np.ndarray = None

    #: Keeps a cached copy of the frame stack IDs.
    _stack_ids: Tuple[str] = None

    #: Keeps a chached copt of the dimension index pointers.
    _dimension_index_pointers: List[BaseTag] = None

    #: Stack ID tag (in integer representation), used to remove any dimension
    #: indices pointing to it.
    STACK_ID_TAG: int = tag_for_keyword("StackID")

    #: Diffusion B-value tag (in integer representation), used to evaluate the
    #: inclusion of a derived volume.
    DERIVED_VOLUME_TAG: int = tag_for_keyword("DiffusionBValue")

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
        self.has_derived_appendix: bool = self.check_derived_appendix()
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
            raise NotImplementedError(MULTIPLE_STACK_IDS)

    def get_frame_functional_groups(self) -> List[Header]:
        """
        Reads per frame functional groups information from the header.

        See Also
        --------
        * :func:`frame_functional_groups`

        Returns
        -------
        List[Header]
            Frame header information
        """
        frames = self.header.get("PerFrameFunctionalGroupsSequence", [])
        if self.has_derived_appendix:
            return self.remove_derived_appendix(frames)
        return frames

    def get_shared_functional_groups(self) -> List[Header]:
        """
        Reads shared functional groups information from the header.

        See Also
        --------
        * :func:`shared_functional_groups`

        Returns
        -------
        List[Header]
            Frame header information
        """
        return self.header.get("SharedFunctionalGroupsSequence", [])

    def check_derived_appendix(self) -> bool:
        """
        Checks whether derived images were appended to the pixel array
        (Phillips) specific functionality.

        Returns
        -------
        bool
            Image had appended derived images
        """
        frames = self.header.get("PerFrameFunctionalGroupsSequence", [])
        try:
            return frames[0].get(PHILLIPS_APPENDIX_FLAG, False)
        except IndexError:
            raise DicomParsingError(MISSING_FUNCTIONAL_GROUPS)

    def check_frame_inclusion(self, frame_info: Header) -> bool:
        """
        Checks whether a frame functional groups header should be included.

        Parameters
        ----------
        frame_info : Header
            Single frame functional groups header

        Returns
        -------
        bool
            Whether this frame should be included in the data (not an
            appendix), or not
        """
        try:
            diffusion_sequence = frame_info["MRDiffusionSequence"][0]
        except (KeyError, IndexError):
            raise DicomParsingError(INVALID_DIFFUSION_SEQUENCE)
        else:
            directionality = diffusion_sequence["DiffusionDirectionality"]
            return directionality != "ISOTROPIC"

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
            raise DicomParsingError(AMBIGUOUS_N_FRAMES)
        return header_n_frames

    def get_frame_index(self, frame_info: Header) -> Tuple[int, int, int]:
        """
        Reads a single frame's index from its associated functional groups
        header information.

        Parameters
        ----------
        frame_info : Header
            Single frame functional groups header information

        Returns
        -------
        Tuple[int, int, int]
            Frame index

        Raises
        ------
        DicomParsingError
            Missing header information
        """
        try:
            frame_content = frame_info["FrameContentSequence"][0]
            return frame_content["DimensionIndexValues"]
        except (IndexError, KeyError):
            raise DicomParsingError(MISSING_FRAME_INDEX)

    def get_frame_stack_id(self, frame_info: Header) -> str:
        """
        Reads a single frame's stack ID from its associated functional groups
        header information.

        Parameters
        ----------
        frame_info : Header
            Single frame functional groups header information

        Returns
        -------
        str
            Stack ID

        Raises
        ------
        DicomParsingError
            Missing header information
        """
        try:
            frame_content = frame_info["FrameContentSequence"][0]
            return frame_content["StackID"]
        except (IndexError, KeyError):
            raise DicomParsingError(MISSING_STACK_ID)

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
            message = MISSING_DIMENSION_INDEX_POINTERS.format(exception=e)
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
        indices = [
            self.get_frame_index(frame_info)
            for frame_info in self.frame_functional_groups
        ]
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
                raise DicomParsingError(MISSING_DERIVED_INDICES)
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
            self.get_frame_stack_id(frame_info)
            for frame_info in self.frame_functional_groups
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
            message = SHAPE_MISMATCH.format(
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
            self._frame_functional_groups = self.get_frame_functional_groups()
        return self._frame_functional_groups

    @property
    def shared_functional_groups(self) -> int:
        """
        Keeps a cached reference to shared header information.

        See Also
        --------
        * :func:`get_shared_functional_groups`

        Returns
        -------
        List[Header]
            Shared header information
        """
        if self._shared_functional_groups is None:
            self._shared_functional_groups = self._shared_functional_groups()
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
