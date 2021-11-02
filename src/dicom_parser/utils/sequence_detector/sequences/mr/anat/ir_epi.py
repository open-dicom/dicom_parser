IR_EPI_RULES = [
    {
        "key": "ScanningSequence",
        "value": ("Echo Planar", "Inversion Recovery"),
        "lookup": "exact",
    },
    {
        "key": "SequenceVariant",
        "value": [
            "Segmented k-Space",
            "Spoiled",
            "MAG Prepared",
        ],
        "lookup": "in",
    },
    {
        "key": "ScanOptions",
        "value": ["IR", "FS"],
        "lookup": "in",
    },
]
