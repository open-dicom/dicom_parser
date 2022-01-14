TIRM_RULES = [
    {
        "key": "ScanningSequence",
        "value": ("Spin Echo", "Inversion Recovery"),
        "lookup": "exact",
    },
    {
        "key": "SequenceVariant",
        "value": (
            "Segmented k-Space",
            "Spoiled",
            "MAG Prepared",
            "Oversampling Phase",
        ),
        "lookup": "exact",
    },
    {
        "key": "ScanOptions",
        "value": ("IR", "SAT1"),
        "lookup": "exact",
    },
]
