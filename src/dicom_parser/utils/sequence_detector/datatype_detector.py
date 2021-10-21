"""
Definition of the :class:`SequenceDetector` class.
"""
from dicom_parser.utils.sequence_detector.messages import (
    INVALID_MODALITY,
    WRONG_DEFINITION_TYPE,
)
from dicom_parser.utils.sequence_detector.data_types import DATA_TYPES
from typing import Tuple


class DatatypeDetector:
    """
    Default data types detector implementation.
    """

    REQUIRED_RULE_KEYS: Tuple[str] = "key", "value"
    DEFAULT_OPERATOR: str = "and"
    DEFAULT_LOOKUP: str = "exact"

    def __init__(self, data_types: dict = None):
        """
        Initializes a new instance of this class.

        Parameters
        ----------
        sequences : dict, optional
            Dictionary of known data types by modality, by default None
        """
        self.data_types = data_types or DATA_TYPES

    def check_definition(self, definition, values: dict) -> bool:
        """
        Checks whether the specified header information values satisfy the
        provided definition.

        Parameters
        ----------
        definition : dict or list
            The imaging sequence definition, as a dict or list of dict
            instances
        values : dict
            Header information provided for the comparison

        Returns
        -------
        bool
            Whether the given header information fits the definition.

        Raises
        ------
        TypeError
            Encountered a definition of an invalid type.
        """
        if not values:
            return None

        # Fix the values as returned from the header to comply with the
        # definition standards.
        values = {
            key: set(value) if isinstance(value, tuple) else {value}
            for key, value in values.items()
        }

        # All definitions are dictionary of rules and operators.
        # Raise error otherwise.
        if (
            not isinstance(definition, dict)
            or "rules" not in definition.keys()
        ):
            raise TypeError(
                WRONG_DEFINITION_TYPE.format(definition_type=type(definition))
            )

        rules_evaluations = []
        for rule in definition["rules"]:
            for key in self.REQUIRED_RULE_KEYS:
                if key not in rule.keys():
                    raise ValueError(f"Missing key {key} in definition rule.")
            lookup = rule.get("lookup", self.DEFAULT_LOOKUP)
            operator = rule.get("operator", self.DEFAULT_OPERATOR)
            evaluation = values.get(key)

    def get_known_modality_sequences(self, modality: str) -> dict:
        """
        Returns a dictionary of imaging sequence definitions.

        Parameters
        ----------
        modality : str
            The modality for which to return imaging sequence defitions

        Returns
        -------
        dict
            Imaging sequence definitions

        Raises
        ------
        NotImplementedError
            The `data_types` dictionary does not include the provided modality
        """
        try:
            return self.data_types[modality]
        except KeyError:
            message = INVALID_MODALITY.format(modality=modality)
            raise NotImplementedError(message)

    def detect(self, modality: str, values: dict) -> str:
        """
        Tries to detect the imaging sequence according to the modality and
        provided header information.

        Parameters
        ----------
        modality : str
            The imaging modality as described in the DICOM header
        values : dict
            Sequence identifying header elements

        Returns
        -------
        str
            The detected sequence name or None.
        """
        known_data_types = self.get_known_modality_sequences(modality)
        for label, definition in known_data_types.items():
            match = self.check_definition(definition, values)
            if match:
                break
        else:
            return None
        return label
