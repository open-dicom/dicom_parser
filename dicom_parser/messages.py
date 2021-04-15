"""
Strings and string formatting templates used in this module.
"""


DATA_READ_FAILURE = (
    "Failed to read image data with the following exception:\n{exception}"
)
EMPTY_SERIES_DIRECTORY = (
    "Could not locate any files within the provided series directory!"
)
INVALID_ELEMENT_IDENTIFIER = "Invalid data element identifier: {tag_or_keyword} of type {input_type}!\nData elements may only be queried using a string representing a keyword or a tuple of two strings representing a tag!"
INVALID_INDEXING_OPERATOR = "Invalid indexing operator value ({key})! Must be of type str, tuple, int, or slice."
INVALID_SERIES_DIRECTORY = "Series instances must be initialized with a valid directory path! Could not locate directory {path}."

# flake8: noqa: E501
