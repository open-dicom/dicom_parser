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
                "value": ["IR", "WE"],
                "lookup": "in",
            },
        ]
    },
    "ir_epi": {
        "rules": [
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
    },
    "t2w": {
        "rules": [
            {
                "key": "ScanningSequence",
                "value": "Spin Echo",
                "lookup": "exact",
            },
            {
                "key": "SequenceVariant",
                "value": ("Segmented k-Space", "Spoiled"),
                "lookup": "exact",
            },
        ]
    },
    "flair": {
        "rules": [
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
    },
    "bold": {
        "rules": [
            {
                "key": "ScanningSequence",
                "value": "Echo Planar",
                "lookup": "exact",
            },
            {
                "key": "ImageType",
                "value": ("ORIGINAL", "PRIMARY", "M", "MB", "ND", "MOSAIC"),
                "lookup": "exact",
            },
        ],
    },
    "func_sbref": {
        "rules": [
            {
                "key": "ScanningSequence",
                "value": "Echo Planar",
                "lookup": "exact",
            },
            {
                "key": "SequenceVariant",
                "value": ["Steady State"],
                "lookup": "in",
            },
            {
                "key": "ImageType",
                "value": ("ORIGINAL", "PRIMARY", "M", "ND", "MOSAIC"),
                "lookup": "exact",
            },
            {
                "key": "ScanOptions",
                "value": ("PFP", "FS"),
                "lookup": "exact",
            },
        ],
    },
    "func_fieldmap": {
        "rules": [
            {
                "key": "ScanningSequence",
                "value": "Echo Planar",
                "lookup": "exact",
            },
            {
                "key": "SequenceVariant",
                "value": ("Segmented k-Space", "Oversampling Phase"),
                "lookup": "exact",
            },
            {
                "key": "ImageType",
                "value": ("ORIGINAL", "PRIMARY", "M", "ND", "MOSAIC"),
                "lookup": "exact",
            },
            {
                "key": "ScanOptions",
                "value": ("PFP", "FS"),
                "lookup": "exact",
            },
        ],
    },
    "dwi": {
        "rules": [
            {
                "key": "ScanningSequence",
                "value": "Echo Planar",
                "lookup": "exact",
            },
            {
                "key": "ImageType",
                "value": (
                    "ORIGINAL",
                    "PRIMARY",
                    "DIFFUSION",
                    "NONE",
                    "MB",
                    "ND",
                    "MOSAIC",
                ),
                "lookup": "exact",
            },
            {
                "key": "ScanOptions",
                "value": "PFP",
                "lookup": "exact",
            },
        ],
    },
    "dwi_fieldmap": {
        "rules": [
            {
                "key": "ScanningSequence",
                "value": "Echo Planar",
                "lookup": "exact",
            },
            {
                "key": "ImageType",
                "value": ("ORIGINAL", "PRIMARY", "M", "ND", "MOSAIC"),
                "lookup": "exact",
            },
            {
                "key": "ScanOptions",
                "value": "PFP",
                "lookup": "exact",
            },
        ],
    },
    "localizer": {
        "rules": [
            {
                "key": "ScanningSequence",
                "value": "Gradient Recalled",
                "lookup": "exact",
            },
            {
                "key": "SequenceVariant",
                "value": ("Spoiled", "Oversampling Phase"),
                "lookup": "exact",
            },
            {
                "key": "ImageType",
                "value": ("ORIGINAL", "PRIMARY", "M", "NORM", "DIS2D"),
                "lookup": "exact",
            },
        ],
    },
}


#: Known sequences by modality.
SEQUENCES = {"Magnetic Resonance": MR_SEQUENCES}
