BOLD_RULES_1 = [
    {
        "key": "ScanningSequence",
        "value": "Echo Planar",
        "lookup": "exact",
    },
    {
        "key": "ImageType",
        "value": [
            ("ORIGINAL", "PRIMARY", "M", "MB", "ND", "MOSAIC"),
            ("ORIGINAL", "PRIMARY", "M", "MB", "ND", "NORM", "MOSAIC"),
        ],
        "lookup": "exact",
        "operator": "any",
    },
]
BOLD_RULES_2 = [
    {
        "key": "ScanningSequence",
        "value": ("Echo Planar", "Gradient Recalled"),
        "lookup": "exact",
    },
    {
        "key": "SequenceVariant",
        "value": "Steady State",
        "lookup": "exact",
    },
    {
        "key": "ImageType",
        "value": ("ORIGINAL", "PRIMARY", "EPI", "NONE"),
        "lookup": "exact",
    },
    {
        "key": "ScanOptions",
        "value": ("EPI_GEMS", "ACC_GEMS"),
        "lookup": "exact",
    },
]
BOLD_RULES = (BOLD_RULES_1, BOLD_RULES_2)
