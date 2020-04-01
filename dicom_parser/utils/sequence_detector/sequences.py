"""
Known sequences defined by the expected (parsed) data element values from the header.

"""

MR_SEQUENCES = {
    "Localizer": {
        "ScanningSequence": {"Gradient Recalled"},
        "SequenceVariant": {"Spoiled", "Oversampling Phase"},
    },
    "MPRAGE": {
        "ScanningSequence": {"Gradient Recalled", "Inversion Recovery"},
        "SequenceVariant": {"Segmented k-Space", "Spoiled", "MAG Prepared"},
    },
    "SPGR": {
        "ScanningSequence": {"Gradient Recalled"},
        "SequenceVariant": {"Segmented k-Space", "Spoiled", "Steady State"},
    },
    "FSPGR": {
        "ScanningSequence": {"Gradient Recalled"},
        "SequenceVariant": {"Segmented k-Space", "Steady State"},
    },
    "FLAIR": {
        "ScanningSequence": {"Spin Echo", "Inversion Recovery"},
        "SequenceVariant": {"Segmented k-Space", "Spoiled", "MAG Prepared"},
    },
    "DTI": (
        {"ScanningSequence": {"Echo Planar", "Spin Echo"}, "SequenceVariant": {"None"}},
        {
            "ScanningSequence": {"Echo Planar", "Research Mode"},
            "SequenceVariant": {"None"},
        },
    ),
    "fMRI": (
        {
            "ScanningSequence": {"Echo Planar"},
            "SequenceVariant": {"Segmented k-Space", "Steady State"},
        },
        {
            "ScanningSequence": {"Echo Planar", "Gradient Recalled"},
            "SequenceVariant": {"Steady State"},
        },
    ),
    "IR-EPI": {
        "ScanningSequence": {"Echo Planar", "Inversion Recovery"},
        "SequenceVariant": {
            "Segmented k-Space",
            "Spoiled",
            "MAG Prepared",
            "Oversampling Phase",
        },
    },
    "ep2d": {
        "ScanningSequence": {"Echo Planar"},
        "SequenceVariant": {"Segmented k-Space", "Spoiled"},
    },
    "FSE": {
        "ScanningSequence": {"Spin Echo"},
        "SequenceVariant": {"Segmented k-Space"},
    },
}


SEQUENCES = {"Magnetic Resonance": MR_SEQUENCES}
