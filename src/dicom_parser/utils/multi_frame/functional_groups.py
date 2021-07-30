"""
Definition of the :class:`FunctionalGroups` class.
"""
from typing import Tuple

from dicom_parser.header import Header
from dicom_parser.utils.exceptions import DicomParsingError
from dicom_parser.utils.multi_frame import messages

#: Phillips derived data appendix data element tag.
PHILLIPS_APPENDIX_FLAG: Tuple[float, float] = (0x18, 0x9117)


class FunctionalGroups:
    """
    Represents a single frame's functional groups sequence in a multi-frame
    encoded acquisition.
    """

    def __init__(self, frame_header: Header):
        """
        Initializes a new :class:`FunctionalGroups` instance.

        Parameters
        ----------
        frame_header : Header
            Functional groups frame subheader
        """
        self.frame_header = frame_header

        # The FrameContentSequence is required for "per frame" functional
        # groups (but not for the shared sequence).
        self.content_sequence = self.get_content_sequence()

    def get_content_sequence(self) -> Header:
        """
        Returns a single frame's functional groups sequence's frame content
        information, or `None` for shared functional groups.

        Returns
        -------
        Header
            Frame content sequence

        Raises
        ------
        DicomParsingError
            Failed to read frame content sequence
        """
        try:
            return self.frame_header["FrameContentSequence"][0]
        except (KeyError, IndexError):
            pass

    #
    # Image properties
    #
    def get_pixel_measures(self) -> Header:
        """
        Returns a functional groups sequence's pixel measures, which are used
        to determine voxel sizes.

        Returns
        -------
        Header
            Pixel measures

        Raises
        ------
        DicomParsingError
            Failed to read pixel measures
        """
        try:
            return self.frame_header["PixelMeasuresSequence"][0]
        except (KeyError, IndexError):
            raise DicomParsingError(messages.MISSING_PIXEL_MEASURES)

    def get_pixel_value_transformations(self) -> Header:
        """
        Returns the pixel value transformations that are required for
        rescaling.

        Returns
        -------
        Header
            Pixel value transformations

        Raises
        ------
        DicomParsingError
            Missing pixel value transformations
        """
        try:
            return self.frame_header["PixelValueTransformationSequence"]
        except KeyError:
            raise DicomParsingError(messages.MISSING_TRANSFORMATIONS)

    def get_plane_orientation(self) -> Header:
        """
        Returns the plane orientation sequence.

        Returns
        -------
        Header
            Plane orientation sequence

        Raises
        ------
        DicomParsingError
            Missing plane orientation sequence
        """
        try:
            return self.frame_header["PlaneOrientationSequence"][0]
        except (KeyError, IndexError):
            raise DicomParsingError(messages.MISSING_PLANE_ORIENTATION)

    def get_plane_position(self) -> Header:
        """
        Returns the plane position sequence.

        Returns
        -------
        Header
            Plane position sequence

        Raises
        ------
        DicomParsingError
            Missing plane position sequence
        """
        try:
            return self.frame_header["PlanePositionSequence"][0]
        except (KeyError, IndexError):
            raise DicomParsingError(messages.MISSING_PLANE_POSITION)

    #
    # Frame and stack indices
    #
    def get_index(self) -> Tuple[int, int, int]:
        """
        Reads the group's index from the header information.

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
            return self.content_sequence["DimensionIndexValues"]
        except KeyError:
            raise DicomParsingError(messages.MISSING_FRAME_INDEX)
        except TypeError:
            raise DicomParsingError(messages.MISSING_CONTENT_SEQUENCE)

    def get_stack_id(self) -> str:
        """
        Reads a single frame's stack ID from its associated functional groups
        header information.

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
            return self.content_sequence["StackID"]
        except KeyError:
            raise DicomParsingError(messages.MISSING_STACK_ID)
        except TypeError:
            raise DicomParsingError(messages.MISSING_CONTENT_SEQUENCE)

    #
    # Flagging derived volumed that my be appended to DWI.
    #
    def get_diffusion_sequence(self) -> Header:
        """
        Returns the MR diffusion sequence.

        Returns
        -------
        Header
            MR difussion sequence

        Raises
        ------
        DicomParsingError
            Failed to read MR diffusion sequence
        """
        try:
            return self.frame_header["MRDiffusionSequence"][0]
        except (KeyError, IndexError):
            message = messages.INVALID_DIFFUSION_SEQUENCE
            raise DicomParsingError(message)

    def get_diffusion_directionality(self) -> str:
        """
        Returns the diffusion directionality from the MR diffusion sequence.

        See Also
        --------

        Returns
        -------
        str
            Diffusion directionality
        """
        diffusion_sequence = self.get_diffusion_sequence()
        try:
            return diffusion_sequence["DiffusionDirectionality"]
        except KeyError:
            message = messages.INVALID_DIFFUSION_SEQUENCE
            raise DicomParsingError(message)

    def check_derived(self) -> bool:
        """
        Checks whether this frame is a derivative or a part of the image.

        See Also
        --------
        * :func:`is_appendix`

        Returns
        -------
        bool
            Whether this frame is a derived frame or not
        """
        if self.appendix_flag:
            diffusion_directionality = self.get_diffusion_directionality()
            return diffusion_directionality == "ISOTROPIC"
        return False

    @property
    def is_appendix(self) -> bool:
        """
        Checks whether this frame is a derivative (appended to the image) or a
        part of the image.

        See Also
        --------
        * :func:`check_derived`

        Returns
        -------
        bool
            Whether this frame is a derived frame or not
        """
        return self.check_derived()

    @property
    def appendix_flag(self) -> bool:
        """
        Returns whether the header information includes a tag that would flag
        it as containing derivatives as appended frames.

        Returns
        -------
        bool
            Whether the functional groups header information contains an
            appendix flag or not
        """
        return self.frame_header.get(PHILLIPS_APPENDIX_FLAG, False)
