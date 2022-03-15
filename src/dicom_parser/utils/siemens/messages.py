"""
Messages for the :mod:`~dicom_parser.utils.siemens` module.
"""

#: Message to display for invalid BandwidthPerPixelPhaseEncode value type.
from typing import Any, Iterable

BANDWITH_PER_PIXEL_TYPEERROR: str = "BandwidthPerPixelPhaseEncode must be of type float or bytes, got {bad_type}!"

#: Message to display when trying to use a B matrix which is not symmetric
#: (and therefore invalid).
B_MATRIX_NOT_SYMMETRIC: str = "B matrix must be symmetric. Value:\n{b_matrix}"

#: Message to display for non positive semi-definite B matrix.
INVALID_B_MATRIX: str = (
    "B matrix not positive semi-definite. Value:\n{b_matrix}"
)

#: Message to display for invalid NumberOfImagesInMosaic value type.
N_IMAGES_IN_MOSAIC_TYPEERROR: str = "NumberOfImagesInMosaic must be of type int or bytes, got {value} of type {bad_type}!"

#: Message to display for invalid MosaicRefAcqTimes value type.
ACQUISITION_TIMES_TYPEERROR: str = "MosaicRefAcqTimes must be of type float or bytes, got {value} of type {bad_type}!"

#: Message to display for invalid DiffusionGradientDirection value type.
DIFFUSION_DIRECTION_TYPEERROR: str = "DiffusionGradientDirection must be of type float or bytes, got {value} of type {bad_type}!"

PRIVATE_TYPEERROR: str = "{name} must be of an instance of {valid_types}, got value '{value}' of type {bad_type}!"

#: Message to display if the NumberOfImagesInMosaic field is not set.
MISSING_NUMBER_OF_IMAGES: str = "NumberOfImagesInMosaic header must be set for mosaic type pixel array data."


def bad_private_tag_type(
    name: str, valid_types: Iterable[type], value: Any
) -> str:
    return PRIVATE_TYPEERROR.format(
        name=name, valid_types=valid_types, value=value, bad_type=type(value)
    )


# flake8: noqa: E501
