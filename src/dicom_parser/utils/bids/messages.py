"""
Messages for the :mod:`dicom_parser.utils.bids` module.
"""

UNREGISTERED_DATA_TYPE: str = "{data_type} not registered for BIDS detector."
MISSING_PATIENT_ID: str = "Patient ID could not be found in the provided header information, subject identifier cannot be resolved."
MISSING_SESSION_TIME: str = "Study date/time could not be found in the provided header information, session identifier cannot be resolved."
