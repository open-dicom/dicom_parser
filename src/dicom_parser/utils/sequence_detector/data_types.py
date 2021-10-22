"""
Known data types defined by the expected (parsed) data element values from the
header.
"""

#: Data types used in Magnetic Resonance (MR) imaging and their associated
#: definitions.
MR_DATA_TYPES = {
    "anat": {
        "rules": [
            {
                "key": "SeriesDescription",
                "value": {"t1w", "t2w", "flair", "mprage", "spgr"},
                "lookup": "icontains",
                "operator": "any",
            }
        ],
    },
    "func": {
        "rules": [
            {
                "key": "SeriesDescription",
                "value": {"fmri"},
                "lookup": "icontains",
                "operator": "any",
            }
        ],
    },
    "dwi": {
        "rules": [
            {
                "key": "SeriesDescription",
                "value": {"dmri"},
                "lookup": "icontains",
                "operator": "any",
            },
            {
                "key": "ImageType",
                "value": {"DIFFUSION"},
                "lookup": "in",
                "operator": "any",
            },
        ],
        "operator": "all",
    },
    "fmap": {
        "rules": [
            {
                "key": "SeriesDescription",
                "value": {"dmri", "fieldmap", "spinecho"},
                "lookup": "icontains",
                "operator": "any",
            },
            {
                "key": "ImageType",
                "value": {"DIFFUSION"},
                "lookup": "not in",
                "operator": "any",
            },
        ],
        "operator": "all",
    },
}

#: Known sequences by modality.
DATA_TYPES = {"Magnetic Resonance": MR_DATA_TYPES}
