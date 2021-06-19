"""
Strings and string formatting templates used in this module.
"""
#: Message displayed when a failure occurs to parse a "DA" data element's raw
#: value.
DATE_PARSING_FAILURE = "Failed to parse '{value}' into a valid date object"

#: Message displayed when trying to parse an "SQ" data element directly.
INVALID_SEQUENCE_PARSING = (
    "SequenceOfItems data element values should be assigned externally."
)

#: Message displayed when a failure occurs to parse a "TM" data element's raw
#: value.
TIME_PARSING_FAILURE = "Failed to parse '{value}' into a valid time object"
