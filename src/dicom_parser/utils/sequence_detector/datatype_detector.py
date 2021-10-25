"""
Definition of the :class:`DatatypeDetector` class.
"""
from dicom_parser.utils.sequence_detector.messages import (
    INVALID_MODALITY,
    WRONG_DEFINITION_TYPE,
    INVALID_OPERATOR_OR_LOOKUP,
)
from dicom_parser.utils.sequence_detector.data_types import DATA_TYPES
from dicom_parser.utils.sequence_detector.lookups import LOOKUPS
from dicom_parser.utils.sequence_detector.operators import OPERATORS
from dicom_parser.utils.sequence_detector.sequences import SEQUENCES
from typing import Tuple


class DatatypeDetector:
    """
    Default data types detector implementation.
    """

    REQUIRED_RULE_KEYS: Tuple[str] = "key", "value"
    DEFAULT_OPERATOR: str = "all"
    DEFAULT_LOOKUP: str = "exact"

    def __init__(self, sequences: dict = None):
        """
        Initializes a new instance of this class.

        Parameters
        ----------
        sequences : dict, optional
            Dictionary of known data types by modality, by default None
        """
        self.sequences = sequences or SEQUENCES

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
            lookup_key = rule.get("lookup", self.DEFAULT_LOOKUP)
            lookup_function = LOOKUPS.get(lookup_key)
            if not lookup_function:
                raise NotImplementedError(
                    INVALID_OPERATOR_OR_LOOKUP.format(operator=lookup_key)
                )

            operator_key = rule.get("operator", self.DEFAULT_OPERATOR)
            operator_function = OPERATORS.get(operator_key)
            if not operator_function:
                raise NotImplementedError(
                    INVALID_OPERATOR_OR_LOOKUP.format(operator=operator_key)
                )

            rules_evaluations.append(
                operator_function(
                    lookup_function(values.get(rule["key"]), rule.get("value"))
                )
            )
        print(rules_evaluations)
        definition_operator = definition.get("operator", self.DEFAULT_OPERATOR)
        definition_operator_function = OPERATORS.get(definition_operator)
        if not operator_function:
            raise NotImplementedError(
                INVALID_OPERATOR_OR_LOOKUP.format(operator=definition_operator)
            )
        return definition_operator_function(rules_evaluations)

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
            The `sequences` dictionary does not include the provided modality
        """
        try:
            return self.sequences[modality]
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
        known_sequences = self.get_known_modality_sequences(modality)
        for label, definition in known_sequences.items():
            match = self.check_definition(definition, values)
            if match:
                break
        else:
            return None
        return label
