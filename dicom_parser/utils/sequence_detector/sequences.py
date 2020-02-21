MR_SEQUENCES = {
    "localizer": {"ScanningSequence": ["GR"], "SequenceVariant": ["SP", "OSP"]},
    "mprage": {"ScanningSequence": ["GR", "IR"], "SequenceVariant": ["SK", "SP", "MP"]},
    "spgr": {"ScanningSequence": ["GR"], "SequenceVariant": ["SK", "SP", "SS"]},
    "fspgr": {"ScanningSequence": ["GR"], "SequenceVariant": ["SK", "SS"]},
    "flair": {"ScanningSequence": ["SE", "IR"], "SequenceVariant": ["SK", "SP", "MP"]},
    "dti": [
        {"ScanningSequence": ["EP", "SE"], "SequenceVariant": ["NONE"]},
        {"ScanningSequence": ["EP", "RM"], "SequenceVariant": ["NONE"]},
    ],
    "fmri": [
        {"ScanningSequence": ["EP"], "SequenceVariant": ["SK", "SS"]},
        {"ScanningSequence": ["EP", "GR"], "SequenceVariant": ["SS"]},
    ],
    "irepi": {
        "ScanningSequence": ["EP", "IR"],
        "SequenceVariant": ["SK", "SP", "MP", "OSP"],
    },
    "ep2d": {"ScanningSequence": ["EP"], "SequenceVariant": ["SK", "SP"]},
    "fse": {"ScanningSequence": ["SE"], "SequenceVariant": ["SK"]},
}


SEQUENCES = {"mr": MR_SEQUENCES}
