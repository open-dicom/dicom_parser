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


# flake8: noqa: E501
