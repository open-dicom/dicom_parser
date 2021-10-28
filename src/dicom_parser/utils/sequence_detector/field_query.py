INVALID_CHARACTERS = "!@#$%^&*()_-+="
#: Helper functions for querying specific fields of BIDS specifications


def find_mprage_acq(header: dict) -> str:
    """
    Finds correct value for the "acq" field of BIDS specification for MPRAGE sequences
    Parameters
    ----------
    header : dict
        Dictionary containing DICOM's header.

    Returns
    -------
    str
        Either "corrected" or "uncorrected" in terms of bias field correction.
    """
    image_type = header.get("ImageType")
    return "corrected" if "NORM" in image_type else "uncorrected"


def find_irepi_acq(header: dict) -> str:
    """
    Finds correct value for the "acq" field of BIDS specification for IR-EPI sequences
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
    strips element from BIDS-invalid characters
    Parameters
    ----------
    element : str
        String element intended for a BIDS specification

    Returns
    -------
    str
        The element stripped from invalid characters
    """
    for invalid_characted in INVALID_CHARACTERS:
        element = element.replace(invalid_characted, "")
    return element


def find_task_name(header: dict) -> str:
    """
    Finds correct value for the "task" field of BIDS specification for fMRI sequences
    Parameters
    ----------
    header : dict
        Dictionary containing DICOM's header.

    Returns
    -------
    str
        The task's name.
    """
    description = header.get("SeriesDescription").lower()
    if "rsf" in description:
        task = "rest"
    else:
        task = "".join(
            [strip_element(i).capitalize() for i in description.split("_")]
        )
    return task


def find_phase_encoding(header: dict) -> str:
    """
    Finds correct value for the "dir" field of BIDS specification for EPI sequences
    Parameters
    ----------
    header : dict
        Dictionary containing DICOM's header.

    Returns
    -------
    str
        Phase encoding direction (AP/PA)
    """
    description = header.get("ProtocolName").lower()
    pe = description.split("_")[-1]
    return pe
