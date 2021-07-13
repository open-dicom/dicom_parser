"""
Messages for the :mod:`~dicom_parser.utils.siemens` module.
"""

#: Message to display when trying to use a B matrix which is not symmetric
#: (and therefore invalid).
B_MATRIX_NOT_SYMMETRIC: str = "B matrix must be symmetric. Value:\n{b_matrix}"

#: Message to display for non positive semi-definite B matrix.
INVALID_B_MATRIX: str = (
    "B matrix not positive semi-definite. Value:\n{b_matrix}"
)
