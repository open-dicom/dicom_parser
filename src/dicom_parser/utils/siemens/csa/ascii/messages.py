"""
Messages from the :mod:`~dicom_parser.utils.siemens.csa.ascii` module.
"""
AST_N_TARGETS: str = (
    "Invalid number of AST assignment targets! Expected 1, got {n_targets}."
)
BAD_ASCCONV_TYPE: str = (
    "Atom {el} has type {maker}, but expecting type {expected_type}"
)
UNEXPECTED_LHS: str = "Unexpected LHS element: {target}"
UNEXPECTED_RHS: str = "Unexpected RHS of assignment: {value}"
UNEXPECTED_TARGET: str = "Unexpected target {target} in {el}"
