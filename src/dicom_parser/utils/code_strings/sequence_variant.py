"""
Definition of the :class:`SequenceVariant` class.
"""
from dicom_parser.utils.choice_enum import ChoiceEnum


class SequenceVariant(ChoiceEnum):
    """
    Represents the `Sequence Variant`_ attribute.

    .. _Sequence Variant:
       https://dicom.innolitics.com/ciods/mr-image/mr-image/00180021

    """

    SK = "Segmented k-Space"
    MTC = "Magnetization Transfer Contrast"
    SS = "Steady State"
    TRSS = "Time Reversed Steady State"
    SP = "Spoiled"
    MP = "MAG Prepared"
    OSP = "Oversampling Phase"
    NONE = "None"
