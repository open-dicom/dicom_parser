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
T2W_RULES_1 = [
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
BOLD_RULES_1 = [
    {
        "key": "ScanningSequence",
        "value": "Echo Planar",
        "lookup": "exact",
    },
    {
        "key": "ImageType",
        "value": [
            ("ORIGINAL", "PRIMARY", "M", "MB", "ND", "MOSAIC"),
            ("ORIGINAL", "PRIMARY", "M", "MB", "ND", "NORM", "MOSAIC"),
        ],
        "lookup": "exact",
        "oprator": "any",
    },
]
BOLD_RULES_2 = [
    {
        "key": "ScanningSequence",
        "value": ("Echo Planar", "Gradient Recalled"),
        "lookup": "exact",
    },
    {
        "key": "SequenceVariant",
        "value": "Steady State",
        "lookup": "exact",
    },
    {
        "key": "ImageType",
        "value": ("ORIGINAL", "PRIMARY", "EPI", "NONE"),
        "lookup": "exact",
    },
    {
        "key": "ScanOptions",
        "value": ("EPI_GEMS", "ACC_GEMS"),
        "lookup": "exact",
    },
]
BOLD_RULES = (BOLD_RULES_1, BOLD_RULES_2)
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
DWI_RULES_1 = [
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
            ("ORIGINAL", "PRIMARY", "DIFFUSION", "NONE", "DIS2D", "MOSAIC"),
            ("ORIGINAL", "PRIMARY", "DIFFUSION", "NONE", "DIS2D"),
            ("ORIGINAL", "PRIMARY", "DIFFUSION", "NONE", "ND", "NORM"),
        ],
        "lookup": "exact",
        "operator": "any",
    },
    {
        "key": "ScanOptions",
        "value": ["PFP"],
        "lookup": "in",
    },
]
DWI_RULES_2 = [
    {
        "key": "ScanningSequence",
        "value": ("Echo Planar", "Research Mode"),
        "lookup": "exact",
    },
    {
        "key": "ImageType",
        "value": ("ORIGINAL", "PRIMARY", "OTHER"),
        "lookup": "exact",
    },
    {
        "key": "ScanOptions",
        "value": ("EPI_GEMS", "PFF"),
        "lookup": "exact",
    },
]
DWI_RULES = (DWI_RULES_1, DWI_RULES_2)
DWI_FIELDMAP_RULES = [
    {
        "key": "ScanningSequence",
        "value": "Echo Planar",
        "lookup": "exact",
    },
    {
        "key": "ImageType",
        "value": [
            ("ORIGINAL", "PRIMARY", "M", "ND", "MOSAIC"),
            ("ORIGINAL", "PRIMARY", "PHASE MAP", "ND"),
            ("DERIVED", "PRIMARY", "DIFFUSION", "ADC", "ND", "NORM"),
            ("DERIVED", "PRIMARY", "DIFFUSION", "FA", "ND", "NORM"),
            ("DERIVED", "PRIMARY", "DIFFUSION", "TRACEW", "ND", "NORM"),
        ],
        "lookup": "exact",
        "operator": "any",
    },
    {
        "key": "ScanOptions",
        "value": ["PFP", ""],
        "lookup": "in",
        "operator": "any",
    },
]
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
        "value": ("ORIGINAL", "PRIMARY", "M", "NORM", "DIS2D"),
        "lookup": "exact",
    },
]
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
SPGR_RULES = [
    {
        "key": "ScanningSequence",
        "value": "Gradient Recalled",
        "lookup": "exact",
    },
    {
        "key": "SequenceVariant",
        "value": ("Steady State", "Spoiled"),
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
    "spgr": SPGR_RULES,
    "fspgr": FSPGR_RULES,
    "t2w": T2W_RULES,
}


#: Known sequences by modality.
SEQUENCE_RULES = {"Magnetic Resonance": MR_SEQUENCE_RULES}
