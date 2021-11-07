"""
Utilities for the :mod:`dicom_parser.utils.bids` module.
"""
from typing import Dict, List

# A summary of the unique parts (key/value) pairs that make up the appropriate
# BIDS-compatible file name by data type.
ANATOMICAL_NAME_PARTS: List[str] = ["acq", "ce", "rec", "inv", "run", "part"]
DWI_NAME_PARTS: List[str] = ["acq", "dir", "run", "part"]
FIELDMAP_NAME_PARTS: List[str] = ["acq", "ce", "dir", "run"]
FUNCTIONAL_NAME_PARTS: List[str] = [
    "task",
    "acq",
    "ce",
    "rec",
    "dir",
    "run",
    "echo",
    "part",
]
SBREF_NAME_PARTS: List[str] = ["acq", "dir", "run", "part"]
NAME_PARTS_BY_DATA_TYPE: Dict[str, List[str]] = {
    "anat": ANATOMICAL_NAME_PARTS,
    "func": FUNCTIONAL_NAME_PARTS,
    "dwi": DWI_NAME_PARTS,
    "sbref": SBREF_NAME_PARTS,
    "fmap": FIELDMAP_NAME_PARTS,
}

BIDS_PATH_TEMPLATE: str = (
    "{subject}/{session}/{data_type}/{subject}_{session}{labels}"
)
