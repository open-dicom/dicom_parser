FUNCTIONAL_SBREF_RULES = [
    {
        "key": "ScanningSequence",
        "value": "Echo Planar",
        "lookup": "exact",
    },
    {
        "key": "SequenceVariant",
        "value": ("Segmented k-Space", "Steady State", "Oversampling Phase"),
        "lookup": "exact",
        "operator": "any",
    },
    {
        "key": "ImageType",
        "value": [
            ("ORIGINAL", "PRIMARY", "M", "ND", "MOSAIC"),
        ],
        "lookup": "exact",
        "operator": "any",
    },
]
