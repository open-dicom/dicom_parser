"""
Messages for the :mod:`dicom_parser.utils.multi_frame` module.
"""

#: Ambiguous number of frames.
AMBIGUOUS_N_FRAMES: str = "Ambiguous multi-frame number of frames value! Expected {header_n_frames} frames, but only {n_frame_info} have functional groups information included."

#: Exception message for invalid Phillips appended derived framed within a multi-frame.
INVALID_DIFFUSION_SEQUENCE: str = "Phillips multi-frame encoded diffusion sequence missing MRDiffusionSequence header information."

#: Missing derived volume dimension index pointers.
MISSING_DERIVED_INDICES: str = "Missing derived volume dimension index pointers! Cannot parse multi-frame image data with confidence."

#: Missing dimension index pointers in image header information.
MISSING_DIMENSION_INDEX_POINTERS: str = "Failed to read dimension index pointers for multi-frame image.\nRaised exception:\n{exception}"

#: Missing index in frame functional groups information.
MISSING_FRAME_INDEX: str = (
    "Failed to read frame indices for a multi-frame encoded image."
)

#: Missing per frame functional groups sequences.
MISSING_FUNCTIONAL_GROUPS: str = "Missing per frame functional groups sequence! Multi-frame image parsing is not possible."

#: Missing stack ID in frame functional groups information.
MISSING_STACK_ID: str = (
    "Failed to read stack IDs for a multi-frame encoded image."
)

#: NotImplementedError message to display for multi stack multi-frames.
MULTIPLE_STACK_IDS: str = (
    "Multi-frame parsing for multipls stack IDs is not implemented."
)

#: Message to display for calculated frame/shape mismatch.
SHAPE_MISMATCH: str = "Calculated data shape does not match the number of frame!\nNumber of volumes:\t{n_volumes}\nCalculated number of frames:\t{n_calculated}\nNumber of frame according to the header: {n_frames}"

# flake8: noqa: E501
