"""
Strings and string formatting templates used in this module.
"""

#: Message displayed when an invalid value is passed to the
#: :func:`dicom_parser.utils.read_file.read_file` function.
BAD_FILE_INPUT = "Raw input to header class my be either a pydicom FileDataset instance or the path of a DICOM file as string or pathlib.Path value!"

#: Message displayed when a data element has an invalid VR.
INVALID_VR = (
    "{key} is not a valid DICOM data element value representation (VR)!"
)

#: Message to show if python-magic is not installed.
MUGGLES = """To generate files by mime type, python-magic must be installed.
To install the required version of python-magic, simply run:

pip install dicom_parser[magic]"""

#: Message to display if the user is trying to read mime types from Windows.
WINDOWS = """Unfortunately, DICOM generation by mime type is not supported in
Windows."""

#: Message to display for empty path generation by extension.
EMPTY_BY_EXTENSION: str = (
    "No files with the extensions {extension} detected in {path}!"
)

#: Message to display for empty path generation by mime.
EMPTY_BY_MIME: str = (
    "No files with the application/dicom mime-type detected in {path}!"
)

#: Message to display for an empty directory.
EMPTY_DIRECTORY: str = "No files found in {path}!"

# flake8: noqa: E501
