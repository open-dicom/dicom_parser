FUNCTIONAL_SBREF_RULES = [
    {
        "key": "ScanningSequence",
        "value": "Echo Planar",
        "lookup": "exact",
    },
    {
        "key": "SequenceVariant",
        "value": [
            ("Segmented k-Space", "Steady State"),
            ("Segmented k-Space", "Steady State", "Oversampling Phase"),
        ],
        "lookup": "exact",
        "operator": "any",
    },
    {
        "key": "ImageType",
        "value": [
            ("ORIGINAL", "PRIMARY", "M", "ND", "MOSAIC"),
            ("ORIGINAL", "PRIMARY", "M", "ND", "NORM", "MOSAIC"),
        ],
        "lookup": "exact",
        "operator": "any",
    },
    {
        "key": "ScanOptions",
        "value": ("PFP", "FS"),
        "lookup": "exact",
    },
]
