FSPGR_RULES = [
    {
        "key": "ScanningSequence",
        "value": "Gradient Recalled",
        "lookup": "exact",
    },
    {
        "key": "SequenceVariant",
        "value": ("Steady State", "Spoiled", "Segmented k-Space"),
        "lookup": "exact",
    },
    {
        "key": "ImageType",
        "value": ("ORIGINAL", "PRIMARY", "OTHER"),
        "lookup": "exact",
    },
    {
        "key": "ScanOptions",
        "value": ("FAST_GEMS", "FILTERED_GEMS", "ACC_GEMS"),
        "lookup": "exact",
    },
]
