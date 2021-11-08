DWI_RULES_1 = [
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
            (
                "ORIGINAL",
                "PRIMARY",
                "DIFFUSION",
                "NONE",
                "MB",
                "ND",
                "MOSAIC",
            ),
            (
                "ORIGINAL",
                "PRIMARY",
                "DIFFUSION",
                "NONE",
                "ND",
                "NORM",
                "MOSAIC",
            ),
            ("ORIGINAL", "PRIMARY", "DIFFUSION", "NONE", "DIS2D", "MOSAIC"),
            ("ORIGINAL", "PRIMARY", "DIFFUSION", "NONE", "DIS2D"),
            ("ORIGINAL", "PRIMARY", "DIFFUSION", "NONE", "ND", "NORM"),
        ],
        "lookup": "exact",
        "operator": "any",
    },
    {
        "key": "ScanOptions",
        "value": ["PFP"],
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
