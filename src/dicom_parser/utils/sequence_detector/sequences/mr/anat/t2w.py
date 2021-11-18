T2W_RULES_1 = [
    {
        "key": "ScanningSequence",
        "value": "Spin Echo",
        "lookup": "exact",
    },
    {
        "key": "SequenceVariant",
        "value": [
            ("Segmented k-Space", "Spoiled"),
            ("Segmented k-Space", "Spoiled", "Oversampling Phase"),
        ],
        "lookup": "exact",
        "operator": "any",
    },
]
T2W_RULES_2 = [
    {
        "key": "ScanningSequence",
        "value": "Research Mode",
        "lookup": "exact",
    },
    {
        "key": "SequenceVariant",
        "value": "None",
        "lookup": "exact",
    },
    {
        "key": "ImageType",
        "value": ("ORIGINAL", "PRIMARY", "OTHER"),
        "lookup": "exact",
    },
    {
        "key": "ScanOptions",
        "value": ["FC", "VB_GEMS", "TRF_GEMS"],
        "lookup": "in",
        "operator": "all",
    },
    {
        "key": "ScanOptions",
        "value": ["FC_FREQ_AX_GEMS", "FC_SLICE_AX_GEMS", "SP", "FS"],
        "lookup": "in",
        "operator": "any",
    },
]
T2W_RULES = (T2W_RULES_1, T2W_RULES_2)
