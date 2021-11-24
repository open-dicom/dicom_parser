"""
Helper functions for querying specific header fields in order to scaffold
BIDS-compatible paths.
"""
#: Characters that should not be used in BIDS elements.
INVALID_CHARACTERS: str = "!@#$%^&*()_-+="


def find_mprage_ce(header: dict) -> str:
    """
    Finds correct value for the "ce" field of BIDS specification for MPRAGE
    sequences.

    Parameters
    ----------
    header : dict
        Dictionary containing DICOM's header

    Returns
    -------
    str
        Either "corrected" or "uncorrected" in terms of bias field correction
    """
    image_type = header.get("ImageType", "")
    return "corrected" if "NORM" in image_type else "uncorrected"


def find_irepi_acq(header: dict) -> str:
    """
    Finds correct value for the "acq" field of BIDS specification for IR-EPI
    sequences.

    Parameters
    ----------
    header : dict
        Dictionary containing DICOM's header.

    Returns
    -------
    str
        The Inversion Time specifiec for the specific IR-EPI sequence.
    """
    ti = header.get("InversionTime")
    return str(int(ti)) if ti else None


def strip_element(element: str) -> str:
    """
    strips element from BIDS-invalid characters.

    Parameters
    ----------
    element : str
        String element intended for a BIDS specification

    Returns
    -------
    str
        The element stripped from invalid characters
    """
    for character in INVALID_CHARACTERS:
        element = element.replace(character, "")
    return element


def find_task_name(header: dict) -> str:
    """
    Finds correct value for the "task" field of BIDS specification for fMRI
    sequences.

    Parameters
    ----------
    header : dict
        Dictionary containing DICOM's header.

    Returns
    -------
    str
        The task's name.
    """
    description = header.get("SeriesDescription", "").lower()
    if "rsf" in description:
        task = "rest"
    else:
        task = "".join(
            [strip_element(i).capitalize() for i in description.split("_")]
        )
    return task


PHASE_ENCODINGS = ("ap", "pa", "lr", "rl", "fwd", "rev")


def find_phase_encoding(header: dict) -> str:
    """
    Finds correct value for the "dir" field of BIDS specification for EPI
    sequences.

    Parameters
    ----------
    header : dict
        Dictionary containing DICOM's header.

    Returns
    -------
    str
        Phase encoding direction
    """
    try:
        phase_encoding = header["phase_encoding_direction"]
        return "FWD" if phase_encoding.endswith("-") else "REV"
    except (KeyError, AttributeError):
        try:
            description = header.get("ProtocolName").lower()
            pe = description.split("_")[-1]
            if pe in PHASE_ENCODINGS:
                return pe
        except (AttributeError, IndexError):
            return
