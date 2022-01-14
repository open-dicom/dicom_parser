# Siemens
LOCALIZER_RULES_1 = [
    {
        "key": "ScanningSequence",
        "value": "Gradient Recalled",
        "lookup": "exact",
    },
    {
        "key": "SequenceVariant",
        "value": [("Spoiled", "Oversampling Phase"), "Spoiled"],
        "lookup": "exact",
        "operator": "any",
    },
    {
        "key": "ImageType",
        "value": ["ORIGINAL", "PRIMARY", "M"],
        "lookup": "in",
        "operator": "all",
    },
    {
        "key": "ImageType",
        "value": ["DIS2D", "ND"],
        "lookup": "in",
        "operator": "any",
    },
]
# GE
LOCALIZER_RULES_2 = [
    {
        "key": "ScanningSequence",
        "value": ["Research Mode", "Gradient Recalled"],
        "lookup": "exact",
        "operator": "any",
    },
    {
        "key": "SequenceVariant",
        "value": ["None", ("Steady State", "Segmented k-Space")],
        "lookup": "exact",
        "operator": "any",
    },
    {
        "key": "ImageType",
        "value": ("ORIGINAL", "PRIMARY", "OTHER"),
        "lookup": "exact",
    },
    {
        "key": "ScanOptions",
        "value": ["PFF", ("FAST_GEMS", "SEQ_GEMS", "PFF")],
        "lookup": "exact",
        "operator": "any",
    },
]
LOCALIZER_RULES = (LOCALIZER_RULES_1, LOCALIZER_RULES_2)
