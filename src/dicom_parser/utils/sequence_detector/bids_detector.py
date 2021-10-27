"""
Definition of the :class:`SequenceDetector` class.
"""
from dicom_parser.utils.sequence_detector.messages import (
    INVALID_MODALITY,
    INVALID_SEQUENCE,
    INVALID_SEQUENCE_KEYS,
)
from dicom_parser.utils.sequence_detector.bids_fields import BIDS_FIELDS
from typing import Tuple, Callable
import warnings


class BIDSDetector:
    """
    Default data types detector implementation.
    """

    REQUIRED_BIDS_NAMING_KEYS: Tuple[str] = "data_type", "suffix"

    def __init__(self, bids_fields: dict = None):
        """
        Initializes a new instance of this class.

        Parameters
        ----------
        bids_fields : dict, optional
            Dictionary of known bids fields by modality, by default None
        """
        self.bids_fields = bids_fields or BIDS_FIELDS

    def get_known_modality_bids_fields(self, modality: str) -> dict:
        """
        Returns a dictionary of imaging bids fields definitions.

        Parameters
        ----------
        modality : str
            The modality for which to return imaging sequence defitions

        Returns
        -------
        dict
            Imaging bids fields definitions

        Raises
        ------
        NotImplementedError
            The `bids_fields` dictionary does not include the provided modality
        """
        try:
            return self.bids_fields[modality]
        except KeyError:
            message = INVALID_MODALITY.format(modality=modality)
            raise NotImplementedError(message)

    def validate_sequence_fields(
        self, sequence: str, sequence_bids_fields: dict
    ) -> None:
        """
        Validates the sequence-specific BIDS fields definition
        Parameters
        ----------
        sequence_bids_fields : dict
            Dictionaty with sequence-specific BIDS fields and values
        """
        if not sequence_bids_fields:
            warnings.warn(INVALID_SEQUENCE.format(sequence=sequence))
            return False
        for required_key in self.REQUIRED_BIDS_NAMING_KEYS:
            if not required_key in sequence_bids_fields:
                raise ValueError(
                    INVALID_SEQUENCE_KEYS.format(required_key=required_key)
                )
        return True

    def build_seqeunce_specific_values(
        self, sequence: str, sequence_bids_fields: dict, header: dict
    ) -> dict:
        """
        Fills instance-specific values as required for an appropriate BIDS naming
        Parameters
        ----------
        sequence : str
            Sequence-identifier
        sequence_bids_fields : dict
            Dictionaty with sequence-specific BIDS fields and values

        Returns
        -------
        dict
            Dictionaty with instance-specific BIDS fields and values
        """
        if not self.validate_sequence_fields(sequence, sequence_bids_fields):
            return None
        result = {}
        for key, value in sequence_bids_fields.items():
            result[key] = (
                value if not isinstance(value, Callable) else value(header)
            )
        return result

    def detect(self, modality: str, sequence: str, header: dict) -> dict:
        """
        Tries to detect the appropriate bids fields' values according to the modality and
        provided sequence information.

        Parameters
        ----------
        modality : str
            The imaging modality as described in the DICOM header
        sequence : str
            BIDS-identifying sequence

        Returns
        -------
        str
            The detected BIDS-appropriate fields and values or None.
        """
        known_bids_fields = self.get_known_modality_bids_fields(modality)
        sequence_bids_fields = known_bids_fields.get(sequence)
        return self.build_seqeunce_specific_values(
            sequence, sequence_bids_fields, header
        )
