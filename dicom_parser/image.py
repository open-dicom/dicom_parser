"""
Definition of the Image class, representing a single pair of
:class:`~dicom_parser.header.Header` and data (3D `NumPy <https://numpy.org>`_ array).

"""

import numpy as np

from dicom_parser.data import Data
from dicom_parser.header import Header
from dicom_parser.parser import Parser
from dicom_parser.utils.read_file import read_file


class Image:
    """
    This class represents a single DICOM image (i.e. `.dcm` file) and provides
    unified access to it's header information and data.

    """

    SIEMENS_MOSAIC_FLAG_TAG = "0029", "1009"
    NUMBER_OF_IMAGES_IN_MOSAIC_TAG = "0019", "100a"

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
    def is_fmri(self) -> bool:
        """
        Returns True for fMRI images according to their header information.

        Returns
        -------
        bool
            Whether this image represents fMRI data.
        """

        return self.header.detected_sequence == "fmri"

    def unpack_siemens_mosaic(self) -> np.ndarray:
        pass

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

        if self.header.get(self.SIEMENS_MOSAIC_FLAG_TAG):
            n_images_in_mosaic = self.header.get(self.NUMBER_OF_IMAGES_IN_MOSAIC_TAG)
            image_orientation_patient = self.header.get("ImageOrientationPatient")

            return self._data.fix_siemens_fmri(n_images_in_mosaic)
        return self._data.raw
