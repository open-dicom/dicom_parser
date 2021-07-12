"""
Definition of the :class:`Image` class, representing a single pair of
:class:`~dicom_parser.header.Header` and data (3D `NumPy <https://numpy.org>`_
array).
"""
import warnings
from pathlib import Path
from typing import Tuple, Union

import numpy as np
from pydicom.dataset import FileDataset

from dicom_parser import messages
from dicom_parser.header import Header
from dicom_parser.utils.read_file import read_file
from dicom_parser.utils.siemens.mosaic import Mosaic


class Image:
    """
    This class represents a single DICOM image (i.e. `.dcm` file) and provides
    unified access to it's header information and data.
    """

    def __init__(self, raw: Union[FileDataset, str, Path]):
        """
        The Image class should be initialized with either a string or a
        :class:`~pathlib.Path` instance representing the path of a .dcm file.
        Another option is to initialize it with a :class:`~pydicom.FileDataset`
        instance, however, in that case make sure that the `stop_before_pixels`
        parameter is set to False, otherwise reading pydicom's `pixel_array`
        will fail.

        Parameters
        ----------
        raw : Union[pydicom.dataset.FileDataset, str, pathlib.Path]
            A single DICOM image
        """
        self.raw = read_file(raw, read_data=True)
        self.header = Header(self.raw)
        self.warnings = []
        self._data = self.read_raw_data()

    def read_raw_data(self) -> np.ndarray:
        """
        Reads the pixel array data as returned by pydicom.

        Returns
        -------
        np.ndarray
            Pixel array data
        """
        try:
            return self.raw.pixel_array
        except (AttributeError, ValueError) as exception:
            warning = messages.DATA_READ_FAILURE.format(exception=exception)
            warnings.warn(warning)
            if warning not in self.warnings:
                self.warnings.append(warning)

    def fix_data(self) -> np.ndarray:
        """
        Applies any required transformation to the data.

        Returns
        -------
        np.ndarray
            Pixel array data
        """
        if self.is_mosaic:
            mosaic = Mosaic(self._data, self.header)
            return mosaic.fold()
        return self._data

    def get_default_relative_path(self) -> Path:
        """
        Returns the default relative path for this image within a DICOM
        archive.

        Returns
        -------
        Path
            Default relative path for this image
        """
        patient_uid = self.header.get("PatientID")
        series_uid = self.header.get("SeriesInstanceUID")
        name = str(self.header.get("InstanceNumber", 0)) + ".dcm"
        return Path(patient_uid, series_uid, name)

    def get_image_shape(self) -> Tuple[int, int]:
        """
        Returns the image shape based on header metadata.

        See Also
        --------
        * :func:`image_shape`

        Returns
        -------
        Tuple[int, int]
            Rows, columns
        """
        shape_dict = self.header.get(["Rows", "Columns"])
        shape = tuple(shape_dict.values())
        return None if None in shape else shape

    def get_image_orientation_patient(self) -> np.array:
        """
        Returns the image position and orientation.

        References
        ----------
        * https://dicom.innolitics.com/ciods/mr-image/image-plane/00200037

        See Also
        --------
        * :func:`image_orientation_patient`

        Returns
        -------
        np.array
            Parsed image orientation (patient) attribute information
        """
        values = self.header.get("ImageOrientationPatient")
        if values is not None:
            return np.array(values).reshape(2, 3).T

    def get_slice_normal(self) -> np.array:
        """
        Returns the slice normal.

        See Also
        --------
        * :func:`slice_normal`

        Returns
        -------
        np.array
            Slice normal
        """
        iop = self.image_orientation_patient
        if iop is not None:
            return np.cross(iop[:, 1], iop[:, 0])

    @property
    def image_shape(self) -> Tuple[int, int]:
        """
        Returns the image shape based on header metadata.

        See Also
        --------
        * :func:`get_image_shape`

        Returns
        -------
        Tuple[int, int]
            Rows, columns
        """
        return self.get_image_shape()

    @property
    def image_orientation_patient(self) -> np.array:
        """
        Returns the image position and orientation.

        See Also
        --------
        * :func:`get_image_orientation_patient`

        Returns
        -------
        np.array
            Parsed image orientation (patient) attribute information
        """
        return self.get_image_orientation_patient()

    @property
    def slice_normal(self) -> np.array:
        """
        Returns the slice normal.

        See Also
        --------
        * :func:`get_slice_normal`

        Returns
        -------
        np.array
            Slice normal
        """
        return self.get_slice_normal()

    @property
    def is_mosaic(self) -> bool:
        """
        Checks whether a 3D volume is encoded as a 2D Mosaic.
        For more information, see the
        :class:`~dicom_parser.utils.siemens.mosaic.Mosaic`
        class.

        Returns
        -------
        bool
            Whether the image is a mosaic encoded volume
        """
        return "MOSAIC" in self.header.get("ImageType")

    @property
    def is_fmri(self) -> bool:
        """
        Returns True for fMRI images according to their header information.

        Returns
        -------
        bool
            Whether this image represents fMRI data
        """
        return self.header.detected_sequence == "fMRI"

    @property
    def data(self) -> np.ndarray:
        """
        Returns the pixel data array after having applied any required
        transformations.

        Returns
        -------
        np.ndarray
            Pixel data array
        """
        return self.fix_data()

    @property
    def default_relative_path(self) -> Path:
        return self.get_default_relative_path()
