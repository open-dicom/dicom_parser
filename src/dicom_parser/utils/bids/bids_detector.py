"""
Definition of the :class:`BidsDetector` class.
"""
import warnings
from typing import Callable, Tuple

from dicom_parser.utils.bids.messages import (
    MISSING_PATIENT_ID,
    MISSING_SESSION_TIME,
    UNREGISTERED_DATA_TYPE,
)
from dicom_parser.utils.bids.sequence_to_bids import SEQUENCE_TO_BIDS
from dicom_parser.utils.bids.utils import (
    BIDS_PATH_TEMPLATE,
    NAME_PARTS_BY_DATA_TYPE,
)
from dicom_parser.utils.sequence_detector.messages import (
    INVALID_MODALITY,
    INVALID_SEQUENCE,
    INVALID_SEQUENCE_KEYS,
)


class BidsDetector:
    """
    Default data types detector implementation.
    """

    #: Required BIDS key/value pairs for each defined rule.
    REQUIRED_KEYS: Tuple[str] = ("data_type", "suffix")

    # Subject identifier configuration.
    SUBJECT_ID_FIELD: str = "PatientID"
    SUBJECT_IDENTIFIER_TEMPLATE: str = "sub-{subject_id}"

    # Session identifier configuration.
    SESSION_DATE_FIELD: str = "StudyDate"
    SESSION_DATE_FORMAT: str = "%Y%m%d"
    SESSION_TIME_FIELD: str = "StudyTime"
    SESSION_TIME_FORMAT: str = "%H%M"
    SESSION_IDENTIFIER_TEMPLATE: str = "ses-{session_date}{session_time}"

    def __init__(self, sequence_to_bids: dict = None):
        """
        Initializes a new instance of this class.

        Parameters
        ----------
        sequence_to_bids : dict, optional
            Dictionary of BIDS field values by modality and detected sequence,
            by default None
        """
        self.sequence_to_bids = sequence_to_bids or SEQUENCE_TO_BIDS

    def get_modality_fields(self, modality: str) -> dict:
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
            The `sequence_to_bids` dictionary does not include the provided
            modality
        """
        try:
            return self.sequence_to_bids[modality]
        except KeyError:
            message = INVALID_MODALITY.format(modality=modality)
            raise NotImplementedError(message)

    def validate_fields(self, sequence: str, fields: dict) -> None:
        """
        Validates the sequence-specific BIDS fields definition
        Parameters
        ----------
        fields : dict
            Dictionaty with sequence-specific BIDS fields and values
        """
        # Check for unregistered sequences.
        if fields is None:
            warnings.warn(INVALID_SEQUENCE.format(sequence=sequence))
            return False
        # Check for sequences registered as not BIDS compatible, such as
        # derived DWI data.
        if fields is False:
            return False
        for required_key in self.REQUIRED_KEYS:
            if required_key not in fields:
                message = INVALID_SEQUENCE_KEYS.format(
                    required_key=required_key, fields=fields
                )
                raise ValueError(message)
        return True

    def get_field_values(
        self, sequence: str, fields: dict, header: dict
    ) -> dict:
        """
        Fills instance-specific values as required for an appropriate BIDS
        naming.

        Parameters
        ----------
        sequence : str
            Sequence-identifier
        fields : dict
            Dictionaty with sequence-specific BIDS fields and values

        Returns
        -------
        dict
            Dictionaty with instance-specific BIDS fields and values
        """
        if not self.validate_fields(sequence, fields):
            return None
        result = {}
        for key, value in fields.items():
            result[key] = (
                value(header) if isinstance(value, Callable) else value
            )
        return result

    def detect(self, modality: str, sequence: str, header: dict) -> dict:
        """
        Tries to detect the appropriate bids fields' values according to the
        modality and provided sequence information.

        Parameters
        ----------
        modality : str
            The imaging modality as described in the DICOM header
        sequence : str
            BIDS-identifying sequence
        header : dict
            DICOM header information

        Returns
        -------
        str
            The detected BIDS-appropriate fields and values or None
        """
        modality_fields = self.get_modality_fields(modality)
        fields = modality_fields.get(sequence)
        return self.get_field_values(sequence, fields, header)

    def build_anonymized_parts(
        self, modality: str, sequence: str, header: dict
    ) -> Tuple[str, str]:
        field_values = self.detect(modality, sequence, header)
        if field_values is None:
            return None, None
        data_type = field_values.pop("data_type")
        suffix = field_values.pop("suffix")
        try:
            parts = NAME_PARTS_BY_DATA_TYPE[data_type]
        except KeyError:
            message = UNREGISTERED_DATA_TYPE.format(data_type=data_type)
            raise NotImplementedError(message)
        labels = (
            f"{part}-{field_values.get(part)}"
            for part in parts
            if field_values.get(part)
        )
        labels = "_".join(labels)
        if labels != "":
            return data_type, f"_{labels}_{suffix}"
        else:
            return data_type, f"_{suffix}"

    def get_subject_identifier(self, header_info: dict) -> str:
        try:
            subject_id = header_info[self.SUBJECT_ID_FIELD]
        except KeyError:
            raise KeyError(MISSING_PATIENT_ID)
        else:
            return self.SUBJECT_IDENTIFIER_TEMPLATE.format(
                subject_id=subject_id
            )

    def get_session_identifier(self, header_info: dict) -> str:
        try:
            date = header_info[self.SESSION_DATE_FIELD]
            time = header_info[self.SESSION_TIME_FIELD]
        except KeyError:
            raise KeyError(MISSING_SESSION_TIME)
        else:
            session_date = date.strftime(self.SESSION_DATE_FORMAT)
            session_time = time.strftime(self.SESSION_TIME_FORMAT)
            return self.SESSION_IDENTIFIER_TEMPLATE.format(
                session_date=session_date, session_time=session_time
            )

    def build_path(
        self, modality: str, sequence: str, header_info: dict
    ) -> str:
        data_type, labels = self.build_anonymized_parts(
            modality, sequence, header_info
        )
        if data_type is None:
            return None
        subject = self.get_subject_identifier(header_info)
        session = self.get_session_identifier(header_info)
        return BIDS_PATH_TEMPLATE.format(
            subject=subject,
            session=session,
            data_type=data_type,
            labels=labels,
        )
