import pydicom

from pathlib import Path


def read_file(raw_input, read_data: bool = False) -> pydicom.FileDataset:
    """
    Return [pydicom](https://pypi.org/project/pydicom/)'s :class:`~pydicom.FileDataset`
    instance based on the provided input.

    
    Parameters
    ----------
    raw_input : FileDataset, str, or Path
        The DICOM image to be parsed.
    
    read_data : bool
        Whether to include the pixel data or not.
    
    Returns
    -------
    FileDataset
        A pydicom.FileDataset instance.
    """

    if isinstance(raw_input, pydicom.FileDataset):
        return raw_input
    elif isinstance(raw_input, (str, Path)):
        return pydicom.dcmread(str(raw_input), stop_before_pixels=not read_data)
    else:
        raise TypeError(
            "Raw input to header class my be either a pydicom FileDataset instance or the path of a DICOM file as string or pathlib.Path value!"  # noqa E501
        )

