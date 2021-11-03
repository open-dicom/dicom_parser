"""
Messages for the :mod:`dicom_parser.utils.siemens.csa` module.
"""

INVALID_CHECK_BIT: str = "CSA element #{i_tag} has an invalid check bit value: {check_bit}!\nValid values are {valid_values}"
READ_OVERREACH: str = "Invalid item length! Destination {destination} is beyond the maximal length ({max_length})!"
