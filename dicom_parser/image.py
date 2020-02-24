"""
Definition of the Image class, representing a single pair of
:class:`~dicom_parser.header.Header` and data (3D `NumPy <https://numpy.org>`_ array).

"""

import numpy as np

from dicom_parser.data import Data
from dicom_parser.header import Header
from dicom_parser.parser import Parser
from dicom_parser.utils.read_file import read_file
from dicom_parser.utils.siemens.csa.header import CsaHeader
from dicom_parser.utils.siemens.private_tags import (
    MOSAIC_FLAG_TAG,
    SIEMENS_PRIVATE_TAGS,
)


class Image:
    """
    This class represents a single DICOM image (i.e. `.dcm` file) and provides
    unified access to it's header information and data.

    """

    def __init__(self, raw, parser=Parser):
        """
        The Image class should be initialized with either a string or a
        :class:`~pathlib.Path` instance representing the path of a .dcm file.
        Another option is to initialize it with a :class:`~pydicom.FileDataset`
        instance, however, in that case make sure that the `stop_before_pixels`
        parameter is set to False, otherwise reading pydicom's `pixel_array`
        will fail.

        Parameters
        ----------
        raw : str, pathlib.Path, or pydicom.FileDataset
            A single DICOM image.
        parser : type, optional
            An object with a public `parse()` method that may be used to parse
            data elements, by default Parser.
        """

        self.raw = read_file(raw, read_data=True)
        self.header = Header(self.raw, parser=parser)
        self._data = Data(self.raw.pixel_array)

    @property
    def mosaic_pixel_array(self) -> bool:
        return bool(self.header.get(MOSAIC_FLAG_TAG))

    @property
    def is_fmri(self) -> bool:
        """
        Returns True for fMRI images according to their header information.

        Returns
        -------
        bool
            Whether this image represents fMRI data.
        """

        return self.header.detected_sequence == "fmri"

    @property
    def data(self) -> np.ndarray:
        """
        Returns the pixel data array after having applied any required
        transformations.

        Returns
        -------
        np.ndarray
            Pixel data array.
        """

        if self.mosaic_pixel_array:
            dimensions = self.header.get_mosaic_volume_shape()
        return self._data.raw
