FUNCTIONAL_SBREF_RULES = [
    {
        "key": "ScanningSequence",
        "value": "Echo Planar",
        "lookup": "exact",
    },
    {
        "key": "SequenceVariant",
        "value": ["Steady State"],
        "lookup": "in",
    },
    {
        "key": "ImageType",
        "value": ("ORIGINAL", "PRIMARY", "M", "ND", "MOSAIC"),
        "lookup": "exact",
    },
    {
        "key": "ScanOptions",
        "value": ("PFP", "FS"),
        "lookup": "exact",
    },
]
