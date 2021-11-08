"""
Strings and string formatting templates used in this module.
"""
WRONG_DEFINITION_TYPE: str = "Sequence definition must be a dict, a list, or a tuple, not {definition_type}!"
ICONTAINS_TYPE_ERROR: str = "Unable to apply icontains lookup for value-rule pairings of types {value_type}-{rule_type} respectively."
INVALID_MODALITY: str = (
    "The {modality} modality has not been implemented or doesn't exist!"
)
INVALID_OPERATOR_OR_LOOKUP: str = (
    "There is no `{operator}` implementation available yet!"
)

INVALID_SEQUENCE: str = (
    "There is no `{sequence}` BIDS naming definition avaliable yet!"
)
INVALID_SEQUENCE_KEYS: str = "All sequences' BIDS naming schemes must contain `{required_key}` definition, please fix:\n{fields}"
MISSING_RULE_KEY: str = "Missing key {key} in definition rule."

# flake8: noqa: E501
