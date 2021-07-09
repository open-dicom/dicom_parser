"""
Definition of the :class:`ScanningSequence` class.
"""
from dicom_parser.utils.choice_enum import ChoiceEnum


class ScanningSequence(ChoiceEnum):
    """
    Represents the `Scanning Sequence`_ attribute.

    .. _Scanning Sequence:
       https://dicom.innolitics.com/ciods/mr-image/mr-image/00180020

    """

    SE = "Spin Echo"
    IR = "Inversion Recovery"
    GR = "Gradient Recalled"
    EP = "Echo Planar"
    RM = "Research Mode"
