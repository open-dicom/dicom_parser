DWI_FIELDMAP = [
    {
        "key": "ScanningSequence",
        "value": "Echo Planar",
        "lookup": "exact",
    },
    {
        "key": "SequenceVariant",
        "value": [
            ("Segmented k-Space", "Steady State"),
            ("Segmented k-Space", "Spoiled"),
            ("Segmented k-Space", "Spoiled", "Oversampling Phase"),
            ("Segmented k-Space", "Steady State", "Oversampling Phase"),
        ],
        "lookup": "exact",
        "operator": "any",
    },
    {
        "key": "ImageType",
        "value": ["ORIGINAL", "PRIMARY", "DIFFUSION", "NONE"],
        "lookup": "in",
        "operator": "all",
    },
    {
        "key": "phase_encoding_direction",
        "value": "-",
        "lookup": "not in",
    },
]
