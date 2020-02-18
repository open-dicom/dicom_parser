from dicom_parser.utils.choice_enum import ChoiceEnum


class Sex(ChoiceEnum):
    """
    Represents the `Patient's Sex <https://dicom.innolitics.com/ciods/mr-image/mr-image/00100040>`_ attribute.
    
    """

    M = "Male"
    F = "Female"
    O = "Other"
