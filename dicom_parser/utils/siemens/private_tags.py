"""
Siemens specific private tags they may not be accessible by keyword using
`pydicom <https://github.com/pydicom/pydicom>`_.

"""
import array

from dicom_parser.utils.siemens.csa.header import CsaHeader


def parse_siemens_slice_timing(value: bytes) -> list:
    """
    Parses a SIEMENS MR image's slice timing as saved in the private
    (0019, 1029) `MosaicRefAcqTimes`_ tag to a list of floats representing
    slice times in milliseconds.

    .. _MosaicRefAcqTimes: https://en.wikibooks.org/wiki/SPM/Slice_Timing#Siemens_scanners

    Parameters
    ----------
    value : bytes
        SIEMENS private MosaicRefAcqTimes data element

    Returns
    -------
    list
        Slice times in milliseconds
    """

    return [round(slice_time, 5) for slice_time in list(array.array("d", value))]


def parse_siemens_gradient_direction(value: bytes) -> list:
    """
    Parses a SIEMENS MR image's B-vector as represented in the private
    (0019, 100E) `DiffusionGradientDirection`_ DICOM tag.

    .. _DiffusionGradientDirection: https://na-mic.org/wiki/NAMIC_Wiki:DTI:DICOM_for_DWI_and_DTI#Private_vendor:_Siemens

    Parameters
    ----------
    value : bytes
        SIEMENS private DiffusionGradientDirection data element.

    Returns
    -------
    list
        Gradient directions (B-vector)
    """

    return [float(value) for value in list(array.array("d", value))]


def parse_siemens_number_of_slices_in_mosaic(value: bytes) -> int:
    return int.from_bytes(value, byteorder="little")


def parse_siemens_b_matrix(value: bytes) -> list:
    return list(array.array("d", value))


def parse_siemens_bandwith_per_pixel_phase_encode(value: bytes):
    return array.array("d", value)[0]


def parse_siemens_csa_header(value: bytes) -> dict:
    return CsaHeader(value).parsed


SIEMENS_PRIVATE_TAGS = {
    # Csa Headers
    # See: https://nipy.org/nibabel/dicom/siemens_csa.html.
    "CSAImageHeaderType": ("0029", "1008"),
    "CSAImageHeaderVersion": ("0029", "1009"),
    "CSAImageHeaderInfo": ("0029", "1010"),
    "CSASeriesHeaderType": ("0029", "1018"),
    "CSASeriesHeaderVersion": ("0029", "1019"),
    "CSASeriesHeaderInfo": ("0029", "1020"),
    # DTI
    # https://na-mic.org/wiki/NAMIC_Wiki:DTI:DICOM_for_DWI_and_DTI
    "NumberOfImagesInMosaic": ("0019", "100a"),
    "SliceMeasurementDuration": ("0019", "100b"),
    "B_value": ("0019", "100c"),
    "DiffusionDirectionality": ("0019", "100d"),
    "DiffusionGradientDirection": ("0019", "100e"),
    "GradientMode": ("0019", "100f"),
    "B_matrix": ("0019", "1027"),
    "BandwidthPerPixelPhaseEncode": ("0019", "1028"),
    "MosaicRefAcqTimes": ("0019", "1029"),
}
