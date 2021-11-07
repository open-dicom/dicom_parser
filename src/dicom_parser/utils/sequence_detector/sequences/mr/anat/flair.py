FLAIR_RULES_1 = [
    {
        "key": "ScanningSequence",
        "value": ("Spin Echo", "Inversion Recovery"),
        "lookup": "exact",
    },
    {
        "key": "SequenceVariant",
        "value": ("Segmented k-Space", "Spoiled", "MAG Prepared"),
        "lookup": "exact",
    },
]
FLAIR_RULES_2 = [
    {
        "key": "ScanningSequence",
        "value": ("Spin Echo", "Inversion Recovery"),
        "lookup": "exact",
    },
    {
        "key": "SequenceVariant",
        "value": "Segmented k-Space",
        "lookup": "exact",
    },
    {
        "key": "ImageType",
        "value": ("ORIGINAL", "PRIMARY", "OTHER"),
        "lookup": "exact",
    },
    {
        "key": "ScanOptions",
        "value": ("FAST_GEMS", "TRF_GEMS", "FILTERED_GEMS"),
        "lookup": "exact",
    },
]
FLAIR_RULES = (FLAIR_RULES_1, FLAIR_RULES_2)
