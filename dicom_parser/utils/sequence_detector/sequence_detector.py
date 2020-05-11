"""
Definition of the
:class:`~dicom_parser.utils.sequence_detector.sequence_detector.SequenceDetector`
class.

"""

from dicom_parser.utils.sequence_detector.messages import WRONG_DEFINITION_TYPE
from dicom_parser.utils.sequence_detector.sequences import SEQUENCES


class SequenceDetector:
    def __init__(self, sequences: dict = None):
        """
        Initializes the
        :class:`~dicom_parser.utils.sequence_detector.sequence_detector.SequenceDetector`
        class.

        Parameters
        ----------
        sequences : dict, optional
            Dictionary of known sequences by modality, by default None
        """

        self.sequences = sequences or SEQUENCES

    def get_known_modality_sequences(self, modality: str) -> dict:
        """
        Returns a dictionary of imaging sequence definitions.

        Parameters
        ----------
        modality : str
            The modality for which to return imaging sequence defitions.

        Returns
        -------
        dict
            Imaging sequence definitions.

        Raises
        ------
        NotImplementedError
            The `sequences` dictionary does not include the provided modality.
        """

        try:
            return self.sequences[modality]
        except KeyError:
            raise NotImplementedError(
                f"The {modality} modality has not been implemented or doesn't exist!"
            )

    def check_definition(self, definition, values: dict) -> bool:
        """
        Checks whether the specified header information values satisfy the provided
        definition.

        Parameters
        ----------
        definition : dict or list
            The imaging sequence definition, as a dict or list of dict instances.
        values : dict
            Header information provided for the comparison.

        Returns
        -------
        bool
            Whether the given header information fits the definition.

        Raises
        ------
        TypeError
            Encountered a definition of an invalid type.
        """

        # Fix the values as returned from the header to comply with the
        # definition standards.
        if values:
            values = {
                key: set(value) if isinstance(value, list) else {value}
                for key, value in values.items()
            }
        else:
            return None

        if isinstance(definition, dict):
            return values == definition
        elif isinstance(definition, (list, tuple)):
            return values in definition
        raise TypeError(WRONG_DEFINITION_TYPE.format(definition_type=type(definition)))

    def detect(self, modality: str, values: dict) -> str:
        """
        Tries to detect the imaging sequence according to the modality and provided
        header information.

        Parameters
        ----------
        modality : str
            The imaging modality as described in the DICOM header.
        values : dict
            Sequence identifying header elements.

        Returns
        -------
        str
            The detected sequence name or None.
        """

        known_sequences = self.get_known_modality_sequences(modality)
        for sequence_name, sequence_definition in known_sequences.items():
            match = self.check_definition(sequence_definition, values)
            if match:
                break
        else:
            return None
        return sequence_name
