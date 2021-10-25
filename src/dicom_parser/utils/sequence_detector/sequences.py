"""
Known sequences defined by the expected (parsed) data element values from the
header.
"""

#: Sequences used in Magnetic Resonance (MR) imaging and their associated
#: definitions.
MR_SEQUENCES = {
    "mprage": {
        "rules": [
            {
                "key": "ScanningSequence",
                "value": ["Gradient Recalled", "Inversion Recovery"],
                "lookup": "in",
                "operator": "and",
            },
            {
                "key": "SequenceVariant",
                "value": ["Segmented k-Space", "Spoiled", "MAG Prepared"],
                "lookup": "in",
                "operator": "and",
            },
            {
                "key": "ScanOptions",
                "value": ["IR", "WE"],
                "lookup": "in",
                "operator": "and",
            },
        ]
    },
    "t2w": {
        "rules": [
            {
                "key": "ScanningSequence",
                "value": "Spin Echo",
                "lookup": "exact",
                "operator": None,
            },
            {
                "key": "SequenceVariant",
                "value": ("Segmented k-Space", "Spoiled"),
                "lookup": "exact",
                "operator": None,
            },
        ]
    },
    "flair": {
        "rules": [
            {
                "key": "ScanningSequence",
                "value": ("Spin Echo", "Inversion Recovery"),
                "lookup": "exact",
                "operator": None,
            },
            {
                "key": "SequenceVariant",
                "value": ["Segmented k-Space", "Spoiled", "MAG Prepared"],
                "lookup": "in",
                "operator": "and",
            },
        ]
    },
    "bold": {
        "rules": [
            [
                {
                    "key": "ScanningSequence",
                    "value": ["Echo Planar", None],
                    "lookup": "in",
                    "operator": "or",
                },
                {
                    "key": "SequenceVariant",
                    "value": (
                        "Segmented k-Space",
                        "Steady State",
                        "Oversampling Phase",
                    ),
                    "lookup": "in",
                    "operator": "and",
                },
            ],
            [
                {
                    "key": "ScanningSequence",
                    "value": ["Echo Planar", None],
                    "lookup": "in",
                    "operator": "or",
                },
                {
                    "key": "SequenceVariant",
                    "value": (
                        "Segmented k-Space",
                        "Steady State",
                        "Oversampling Phase",
                    ),
                    "lookup": "in",
                    "operator": "and",
                },
            ],
        ]
    },
}


#: Known sequences by modality.
SEQUENCES = {"Magnetic Resonance": MR_SEQUENCES}
