MPRAGE_RULES = [
    {
        "key": "ScanningSequence",
        "value": ("Gradient Recalled", "Inversion Recovery"),
        "lookup": "exact",
    },
    {
        "key": "SequenceVariant",
        "value": ("Segmented k-Space", "Spoiled", "MAG Prepared"),
        "lookup": "exact",
    },
    {
        "key": "ScanOptions",
        "value": ["IR"],
        "lookup": "in",
    },
]
