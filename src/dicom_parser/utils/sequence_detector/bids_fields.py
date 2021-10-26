from dicom_parser.utils.sequence_detector.field_query import (
    find_mprage_acq,
    find_irepi_acq,
    find_task_name,
    find_phase_encoding,
)

#: BIDS fields used in Magnetic Resonance (MR) imaging and their associated
#: definitions.
MR_BIDS_FIELDS = {
    "mprage": {"data_type": "anat", "acq": find_mprage_acq, "suffix": "T1w"},
    "ir_epi": {"data_type": "anat", "acq": find_irepi_acq, "suffix": "IRT1"},
    "t2w": {"data_type": "anat", "acq": find_mprage_acq, "suffix": "T2w"},
    "flair": {"data_type": "anat", "suffix": "FLAIR"},
    "bold": {
        "data_type": "func",
        "task": find_task_name,
        "dir": find_phase_encoding,
        "suffix": "bold",
    },
    "func_sbref": {
        "data_type": "func",
        "task": find_task_name,
        "dir": find_phase_encoding,
        "suffix": "sbref",
    },
    "func_fieldmap": {
        "data_type": "fmap",
        "acq": "func",
        "dir": find_phase_encoding,
        "suffix": "epi",
    },
    "dwi": {
        "data_type": "dwi",
        "dir": find_phase_encoding,
        "suffix": "dwi",
    },
    "dwi_fieldmap": {
        "data_type": "fmap",
        "acq": "dwi",
        "dir": find_phase_encoding,
        "suffix": "epi",
    },
}
#: Known bids fields by modality.
BIDS_FIELDS = {"Magnetic Resonance": MR_BIDS_FIELDS}
