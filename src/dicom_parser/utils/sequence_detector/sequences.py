"""
Known sequences defined by the expected (parsed) data element values from the
header.
"""

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
IREPI_RULES = [
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
T2W_RULES = [
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
FLAIR_RULES = [
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
BOLD_RULES = [
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
]
FUNCTIONAL_SBREF_RULES = [
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
]
FUNCTIONAL_FIELDMAP_RULES = [
    {
        "key": "ScanningSequence",
        "value": "Echo Planar",
        "lookup": "exact",
    },
    {
        "key": "SequenceVariant",
        "value": [
            ("Segmented k-Space", "Oversampling Phase"),
            "Segmented k-Space",
        ],
        "lookup": "exact",
        "operator": "any",
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
]
DWI_RULES = [
    {
        "key": "ScanningSequence",
        "value": "Echo Planar",
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
        ],
        "lookup": "exact",
        "operator": "any",
    },
    {
        "key": "ScanOptions",
        "value": ["PFP", ("PFP", "FS")],
        "lookup": "exact",
        "operator": "any",
    },
]
DWI_FIELDMAP_RULES = [
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
]
LOCALIZER_RULES = [
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
]

#: Sequences used in Magnetic Resonance (MR) imaging and their associated
#: definitions.
MR_SEQUENCE_RULES = {
    "bold": BOLD_RULES,
    "dwi": DWI_RULES,
    "dwi_fieldmap": DWI_FIELDMAP_RULES,
    "flair": FLAIR_RULES,
    "func_fieldmap": FUNCTIONAL_FIELDMAP_RULES,
    "func_sbref": FUNCTIONAL_SBREF_RULES,
    "ir_epi": IREPI_RULES,
    "localizer": LOCALIZER_RULES,
    "mprage": MPRAGE_RULES,
    "t2w": T2W_RULES,
}


#: Known sequences by modality.
SEQUENCE_RULES = {"Magnetic Resonance": MR_SEQUENCE_RULES}
