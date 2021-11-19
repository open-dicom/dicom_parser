DWI_SBREF_RULES = [
    {
        "key": "ScanningSequence",
        "value": "Echo Planar",
        "lookup": "exact",
    },
    {
        "key": "SequenceVariant",
        "value": ("Segmented k-Space", "Steady State"),
        "lookup": "exact",
    },
    {
        "key": "ImageType",
        "value": [
            ("ORIGINAL", "PRIMARY", "M", "ND", "MOSAIC"),
            # ("ORIGINAL", "PRIMARY", "PHASE MAP", "ND"),
        ],
        "lookup": "exact",
        "operator": "any",
    },
    {
        "key": "ScanOptions",
        "value": ["PFP", ""],
        "lookup": "exact",
        "operator": "any",
    },
]
