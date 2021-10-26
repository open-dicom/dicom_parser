"""
Strings and string formatting templates used in this module.
"""
WRONG_DEFINITION_TYPE = "Sequence definition must be a dict, a list, or a tuple, not {definition_type}!"
ICONTAINS_TYPE_ERROR = "Unable to apply icontains lookup for value-rule pairings of types {value_type}-{rule_type} respectively."
INVALID_MODALITY = (
    "The {modality} modality has not been implemented or doesn't exist!"
)
INVALID_OPERATOR_OR_LOOKUP = (
    "There is no `{operator}` implementation available yet!"
)

INVALID_SEQUENCE = (
    "There is no `{sequence}` BIDS naming definition avaliable yet!"
)
INVALID_SEQUENCE_KEYS = "All sequences' BIDS naming schemes must contain `{required_key}` definition."
# flake8: noqa: E501
