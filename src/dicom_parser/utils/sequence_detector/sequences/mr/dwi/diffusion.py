DWI_RULES_1 = [
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
        "lookup": "in",
    },
]
DWI_RULES_2 = [
    {
        "key": "ScanningSequence",
        "value": ("Echo Planar", "Research Mode"),
        "lookup": "exact",
    },
    {
        "key": "ImageType",
        "value": ("ORIGINAL", "PRIMARY", "OTHER"),
        "lookup": "exact",
    },
    {
        "key": "ScanOptions",
        "value": ("EPI_GEMS", "PFF"),
        "lookup": "exact",
    },
]
DWI_RULES = (DWI_RULES_1, DWI_RULES_2)
