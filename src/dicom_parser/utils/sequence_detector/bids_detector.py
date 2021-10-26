"""
Definition of the :class:`SequenceDetector` class.
"""
from dicom_parser.utils.sequence_detector.messages import (
    INVALID_MODALITY,
    WRONG_DEFINITION_TYPE,
    INVALID_OPERATOR_OR_LOOKUP,
)
from dicom_parser.utils.sequence_detector.bids_fields import BIDS_FIELDS


class BIDSDetector:
    """
    Default data types detector implementation.
    """

    REQUIRED_RULE_KEYS: Tuple[str] = "key", "value"
    DEFAULT_OPERATOR: str = "all"
    DEFAULT_LOOKUP: str = "exact"

    # def __init__(self, sequences: dict = None):
    #     """
