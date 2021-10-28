"""
Definition of the :class:`BidsDetector` class.
"""
import warnings
from typing import Callable, Dict, List, Tuple

from dicom_parser.utils.bids.sequence_to_bids import SEQUENCE_TO_BIDS
from dicom_parser.utils.sequence_detector.messages import (
    INVALID_MODALITY,
    INVALID_SEQUENCE,
    INVALID_SEQUENCE_KEYS,
)


class BidsDetector:
    """
    Default data types detector implementation.
    """

    BIDS_FILE_NAME_TEMPLATE: Dict[str, List[str]] = {
        "anat": ["acq", "ce", "rec", "inv", "run", "part"],
        "func": [
            "task",
            "acq",
            "ce",
            "rec",
            "dir",
            "run",
            "echo",
            "part",
        ],
        "dwi": ["acq", "dir", "run", "part"],
        "sbref": ["acq", "dir", "run", "part"],
        "fmap": ["acq", "ce", "dir", "run"],
    }
    BIDS_PATH_TEMPLATE: str = (
        "{subject}/{session}/{data_type}/{subject}_{session}{labels}"
    )
    REQUIRED_BIDS_NAMING_KEYS: Tuple[str] = ("data_type", "suffix")

    def __init__(self, bids_fields: dict = None):
        """
        Initializes a new instance of this class.

        Parameters
        ----------
        bids_fields : dict, optional
            Dictionary of known bids fields by modality, by default None
        """
        self.bids_fields = bids_fields or SEQUENCE_TO_BIDS

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
            The `bids_fields` dictionary does not include the provided modality
        """
        try:
            return self.bids_fields[modality]
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
        if not fields:
            warnings.warn(INVALID_SEQUENCE.format(sequence=sequence))
            return False
        for required_key in self.REQUIRED_BIDS_NAMING_KEYS:
            if required_key not in fields:
                raise ValueError(
                    INVALID_SEQUENCE_KEYS.format(required_key=required_key)
                )
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
            parts = self.BIDS_FILE_NAME_TEMPLATE[data_type]
        except KeyError:
            raise NotImplementedError(
                f"{data_type} not registered for BIDS detector."
            )
        labels = (
            f"{part}-{field_values.get(part)}"
            for part in parts
            if field_values.get(part)
        )
        labels = "_".join(labels)
        if labels != "":
            return data_type, "_" + labels + "_" + suffix
        else:
            return data_type, "_" + suffix

    def build_path(self, modality: str, sequence: str, header: dict) -> str:
        data_type, labels = self.build_anonymized_parts(
            modality, sequence, header
        )
        if (data_type is None) and (labels is None):
            return None
        subject = f"sub-{header.get('PatientID')}"
        session_date = header.get("StudyDate").strftime("%Y%m%d")
        session_time = header.get("StudyTime").strftime("%H%M")
        session = f"ses-{session_date}{session_time}"
        return self.BIDS_PATH_TEMPLATE.format(
            subject=subject,
            session=session,
            data_type=data_type,
            labels=labels,
        )
