"""
Definition of the :class:`SequenceDetector` class.
"""
from typing import Callable, Tuple

from dicom_parser.utils.sequence_detector.lookups import LOOKUPS
from dicom_parser.utils.sequence_detector.messages import (
    INVALID_MODALITY,
    INVALID_OPERATOR_OR_LOOKUP,
    MISSING_RULE_KEY,
    WRONG_DEFINITION_TYPE,
)
from dicom_parser.utils.sequence_detector.operators import OPERATORS
from dicom_parser.utils.sequence_detector.sequences import SEQUENCE_RULES


class SequenceDetector:
    """
    Default data types detector implementation.
    """

    LOOKUP_KEY: str = "lookup"
    OPERATOR_KEY: str = "operator"
    RULES_KEY: str = "rules"

    DEFAULT_LOOKUP: str = "exact"
    DEFAULT_OPERATOR: str = "all"

    REQUIRED_RULE_KEYS: Tuple[str] = ("key", "value")

    def __init__(self, rules: dict = None):
        """
        Initializes a new instance of this class.

        Parameters
        ----------
        rules : dict, optional
            Dictionary of known data types by modality, by default None
        """
        self.rules = rules or SEQUENCE_RULES

    def validate_rule_keys(self, rule: dict) -> None:
        """
        Checks whether the given rule contains all required keys.

        Parameters
        ----------
        rule : dict
            Sequence detection rule

        Raises
        ------
        ValueError
            Missing mandatory rule key
        """
        for key in self.REQUIRED_RULE_KEYS:
            if key not in rule.keys():
                message = MISSING_RULE_KEY.format(key=key)
                raise ValueError(message)

    def retreive_lookup(self, rule: dict) -> Callable:
        """
        Returns the appropriate lookup function for the given rule.

        Parameters
        ----------
        rule : dict
            Sequence detection rule

        Returns
        -------
        Callable
            Lookup function

        Raises
        ------
        NotImplementedError
            No lookup function found
        """
        lookup_key = rule.get(self.LOOKUP_KEY, self.DEFAULT_LOOKUP)
        lookup_function = LOOKUPS.get(lookup_key)
        if not lookup_function:
            raise NotImplementedError(
                INVALID_OPERATOR_OR_LOOKUP.format(operator=lookup_key)
            )
        return lookup_function

    def retreive_operator(self, rule: dict) -> Callable:
        """
        Returns the appropriate operator function for the given rule.

        Parameters
        ----------
        rule : dict
            Sequence detection rule

        Returns
        -------
        Callable
            Operator function

        Raises
        ------
        NotImplementedError
            No operator function found
        """
        operator_key = rule.get(self.OPERATOR_KEY, self.DEFAULT_OPERATOR)
        operator_function = OPERATORS.get(operator_key)
        if not operator_function:
            raise NotImplementedError(
                INVALID_OPERATOR_OR_LOOKUP.format(operator=operator_key)
            )
        return operator_function

    def evaluate_rule(
        self, rule: dict, header_fields: dict, verbose: bool = False
    ) -> bool:
        """
        Evaluates a single sequence categorization rule.

        Parameters
        ----------
        rule : dict
            Sequence categorization rule
        header_fields : dict
            Header information
        verbose : bool
            Whether to show evaluation logs

        Returns
        -------
        bool
            Whether the sequence satisfies the given rule or not
        """
        self.validate_rule_keys(rule)
        key, value = rule["key"], rule["value"]
        lookup = self.retreive_lookup(rule)
        operator = self.retreive_operator(rule)
        header_value = header_fields.get(key)
        if verbose:
            print(f"Evaluating rule:\n{rule}")
            print(f"Queried header value: {header_value}")
        if isinstance(value, list):
            if verbose:
                print(f"Matching each of {value} against the queried value...")
            result = operator(lookup(header_value, v) for v in value)
        else:
            if verbose:
                print(f"Matching {value} against the header metadata...")
            result = lookup(header_value, value)
        if verbose:
            result_text = "MATCH" if result else "NO MATCH"
            print(result_text)
        return result

    def check_definition(
        self, definition, header_fields: dict, verbose: bool = False
    ) -> bool:
        """
        Checks whether the specified header information values satisfy the
        provided definition.

        Parameters
        ----------
        definition : dict or list
            The imaging sequence definition, as a dict or list of dict
            instances
        header_fields : dict
            Header information provided for the comparison
        verbose : bool
            Whether to show evaluation logs

        Returns
        -------
        bool
            Whether the given header information fits the definition.

        Raises
        ------
        TypeError
            Encountered a definition of an invalid type.
        """
        if not header_fields:
            return None

        # All definitions are dictionary of rules and operators.
        # Raise error otherwise.
        if not isinstance(definition, (dict, list, tuple)):
            message = WRONG_DEFINITION_TYPE.format(
                definition_type=type(definition)
            )
            raise TypeError(message)
        if isinstance(definition, tuple):
            return any(
                self.check_definition(d, header_fields, verbose=verbose)
                for d in definition
            )
        rules = (
            definition.get(self.RULES_KEY, [])
            if isinstance(definition, dict)
            else definition
        )
        rules_evaluations = (
            self.evaluate_rule(rule, header_fields, verbose=verbose)
            for rule in rules
        )
        operator = (
            definition.get(self.OPERATOR_KEY, self.DEFAULT_OPERATOR)
            if isinstance(definition, dict)
            else self.DEFAULT_OPERATOR
        )
        operator = OPERATORS.get(operator)
        if not operator:
            message = INVALID_OPERATOR_OR_LOOKUP.format(operator=operator)
            raise NotImplementedError(message)
        return operator(rules_evaluations)

    def get_modality_rules(self, modality: str) -> dict:
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
            return self.rules[modality]
        except KeyError:
            message = INVALID_MODALITY.format(modality=modality)
            raise NotImplementedError(message)

    def detect(
        self, modality: str, values: dict, verbose: bool = False
    ) -> str:
        """
        Tries to detect the imaging sequence according to the modality and
        provided header information.

        Parameters
        ----------
        modality : str
            The imaging modality as described in the DICOM header
        values : dict
            Sequence identifying header elements
        verbose : bool
            Whether to show evaluation logs

        Returns
        -------
        str
            The detected sequence name or None.
        """
        rules = self.get_modality_rules(modality)
        for label, definition in rules.items():
            if verbose:
                print(f"\nEvaluating {label} rules:")
            match = self.check_definition(definition, values, verbose=verbose)
            if match:
                return label
