FUNCTIONAL_FIELDMAP_RULES = [
    {
        "key": "ScanningSequence",
        "value": "Echo Planar",
        "lookup": "exact",
    },
    {
        "key": "SequenceVariant",
        "value": [
            ("Segmented k-Space", "Oversampling Phase"),
            "Segmented k-Space",
        ],
        "lookup": "exact",
        "operator": "any",
    },
    {
        "key": "ImageType",
        "value": ("ORIGINAL", "PRIMARY", "M", "ND", "MOSAIC"),
        "lookup": "exact",
    },
    {
        "key": "ScanOptions",
        "value": [("PFP", "FS"), "FS"],
        "lookup": "exact",
        "operator": "any",
    },
]
