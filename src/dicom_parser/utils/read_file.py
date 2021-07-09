"""
Definition of the :func:`read_file` function.
"""
from pathlib import Path
from typing import Union

import pydicom
from dicom_parser.utils.messages import BAD_FILE_INPUT
from pydicom.dataset import FileDataset


def read_file(
    raw_input: Union[FileDataset, str, Path], read_data: bool = False
) -> pydicom.FileDataset:
    """
    Return pydicom_'s :class:`~pydicom.dataset.FileDataset` instance based on
    the provided input.

    .. _pydicom:
       https://pypi.org/project/pydicom/

    Parameters
    ----------
    raw_input : Union[FileDataset, str, Path]
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
        return pydicom.dcmread(
            str(raw_input), stop_before_pixels=not read_data
        )
    else:
        raise TypeError(BAD_FILE_INPUT)
