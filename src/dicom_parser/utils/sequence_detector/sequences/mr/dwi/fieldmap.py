DWI_FIELDMAP_RULES = [
    {
        "key": "ScanningSequence",
        "value": "Echo Planar",
        "lookup": "exact",
    },
    {
        "key": "ImageType",
        "value": [
            ("ORIGINAL", "PRIMARY", "M", "ND", "MOSAIC"),
            ("ORIGINAL", "PRIMARY", "PHASE MAP", "ND"),
            ("DERIVED", "PRIMARY", "DIFFUSION", "ADC", "ND", "NORM"),
            ("DERIVED", "PRIMARY", "DIFFUSION", "FA", "ND", "NORM"),
            ("DERIVED", "PRIMARY", "DIFFUSION", "TRACEW", "ND", "NORM"),
        ],
        "lookup": "exact",
        "operator": "any",
    },
    {
        "key": "ScanOptions",
        "value": ["PFP", ""],
        "lookup": "in",
        "operator": "any",
    },
]
