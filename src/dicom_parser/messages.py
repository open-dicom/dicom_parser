"""
Strings and string formatting templates used in this module.
"""

BAD_ROTATION_MATRIX: str = "Rotation matrix not nearly orthogonal."
DATA_READ_FAILURE: str = (
    "Failed to read image data with the following exception:\n{exception}"
)
INVALID_ELEMENT_IDENTIFIER: str = "Invalid data element identifier: {tag_or_keyword} of type {input_type}!\nData elements may only be queried using a string representing a keyword or a tuple of two strings representing a tag!"
INVALID_INDEXING_OPERATOR: str = "Invalid indexing operator value ({key})! Must be of type str, tuple, int, or slice."
INVALID_SERIES_DIRECTORY: str = "Series instances must be initialized with a valid directory path! Could not locate directory {path}."
UNREGISTERED_MODALITY: str = (
    "No sequence identifiers registered for {modality}!"
)
MISSING_HEADER_INFO: str = "No header information found for {modality} sequence detection using {keys}!"
MISSING_SERIES_SOURCE: str = "Series instances must be initialized with a path or an iterable of image instances!"

# flake8: noqa: E501
