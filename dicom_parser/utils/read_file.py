import pydicom

from pathlib import Path


def read_file(raw_input, read_data: bool = False) -> pydicom.FileDataset:
    """
    Return pydicom_'s :class:`~pydicom.dataset.FileDataset` instance based on the provided
    input.

    .. _pydicom: https://pypi.org/project/pydicom/

    Parameters
    ----------
    raw_input : :class:`~pydicom.dataset.FileDataset`, str, or Path
        The DICOM image to be parsed

    read_data : bool
        Whether to include the pixel data or not

    Returns
    -------
    :class:`~pydicom.dataset.FileDataset`
        Image data
    """

    if isinstance(raw_input, pydicom.Dataset):
        return raw_input
    elif isinstance(raw_input, (str, Path)):
        return pydicom.dcmread(str(raw_input), stop_before_pixels=not read_data)
    else:
        raise TypeError(
            "Raw input to header class my be either a pydicom FileDataset instance or the path of a DICOM file as string or pathlib.Path value!"  # noqa E501
        )
