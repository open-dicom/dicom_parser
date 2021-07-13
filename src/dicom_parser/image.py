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
from dicom_parser.utils.exceptions import PrecisionError
from dicom_parser.utils.read_file import read_file
from dicom_parser.utils.siemens.mosaic import Mosaic
from dicom_parser.utils.siemens.private_tags import (
    b_matrix_to_q_vector,
    nearest_pos_semi_def,
)


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

        self.number = self.header.get("InstanceNumber")
        self.position = self.header.get("ImagePositionPatient")

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

    def rescale_data(self, data: np.array) -> np.array:
        """
        Rescales the provided *data* pixel array using the `Rescale Slope`_ and
        `Rescale Intercept`_ header fields.

        .. _Rescale Intercept:
           https://dicom.innolitics.com/ciods/enhanced-mr-image/enhanced-mr-image-multi-frame-functional-groups/52009229/00289145/00281052
        .. _Rescale Slope:
           https://dicom.innolitics.com/ciods/enhanced-mr-color-image/enhanced-mr-color-image-multi-frame-functional-groups/52009229/00289145/00281053

        Parameters
        ----------
        data : np.array
            Pixel array

        Returns
        -------
        np.array
            Fixed pixel array
        """
        slope = self.header.get("RescaleSlope", 1)
        intercept = self.header.get("RescaleIntercept", 0)
        return data * slope + intercept

    def fix_data(self) -> np.ndarray:
        """
        Applies any required transformation to the data.

        See Also
        --------
        * :func:`rescale_data`
        * :class:`~dicom_parser.utils.siemens.mosaic.Mosaic`

        Returns
        -------
        np.ndarray
            Fixed pixel array data
        """
        if self.is_mosaic:
            mosaic = Mosaic(self._data, self.header)
            return mosaic.fold()
        return self.rescale_data(self._data)

    def get_default_relative_path(self) -> Path:
        """
        Returns the default relative path for this image within a DICOM
        archive.

        See Also
        --------
        * :func:`default_relative_path`

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
        # TODO: Implement Siemens fix for slice normal?
        # https://github.com/nipy/nibabel/blob/62aea04248e70d7c4529954ca41685d7f75a0b1e/nibabel/nicom/dicomwrappers.py#L710

    def get_rotation_matrix(self) -> np.array:
        """
        Returns the rotation matrix between array indices and mm.

        References
        ----------
        * https://nipy.org/nibabel/dicom/dicom_orientation.html

        Returns
        -------
        np.array
            Rotation matrix

        Raises
        ------
        PrecisionError
            Unorthogonal rotation matrix
        """
        iop = self.image_orientation_patient
        s_norm = self.slice_normal
        if iop is None or s_norm is None:
            return None
        rotation = np.eye(3)
        rotation[:, :2] = np.fliplr(iop)
        rotation[:, 2] = s_norm
        precision = np.allclose(
            np.eye(3), np.dot(rotation, rotation.T), atol=5e-5
        )
        if not precision:
            raise PrecisionError(messages.BAD_ROTATION_MATRIX)
        return rotation

    def get_spatial_resolution(self) -> Tuple[float]:
        """
        Returns the spatial resolution of the image in millimeters.

        See Also
        --------
        * :func:`spatial_resolution`

        Returns
        -------
        Tuple[float]
            Spatial resolution in millimeters
        """
        pixel_spacing = list(self.header.get("PixelSpacing"))
        slice_thickness = self.header.get("SliceThickness")
        if slice_thickness:
            pixel_spacing.append(slice_thickness)
        return tuple(pixel_spacing)

    def get_affine(self) -> np.array:
        """
        Returns the affine transformation of this image.

        See Also
        --------
        * :func:`affine`

        Returns
        -------
        np.array
            Affine transformation matrix
        """
        rotation = self.rotation_matrix
        resolution = self.spatial_resolution
        required = (rotation, resolution, self.position)
        if any([value is None for value in required]):
            return None
        affine = np.eye(4)
        affine[:3, :3] = rotation * np.array(resolution)
        affine[:3, 3] = self.position
        return affine

    def get_b_matrix(self) -> np.ndarray:
        """
        Returns the B matrix of Siemens scans.

        See Also
        --------
        :func:`~dicom_parser.utils.siemens.private_tags.parse_siemens_b_matrix`
        :func:`b_matrix`

        Returns
        -------
        np.ndarray
            B matrix
        """
        return self.header.get("B_matrix")

    def get_q_vector(self) -> np.ndarray:
        """
        Calculates Siemens DWI q-vector in voxel space.

        See Also
        --------
        * :func:`~dicom_parser.utils.siemens.private_tags.b_matrix_to_q_vector`
        * :func:`q_vector`

        Returns
        -------
        np.ndarray
            q-vector
        """
        return b_matrix_to_q_vector(self.voxel_space_b_matrix)

    def get_voxel_space_b_matrix(self) -> np.ndarray:
        """
        Returns the B matrix in voxel space (rather than patient space).

        See Also
        --------
        * :func:`voxel_space_b_matrix`

        Returns
        -------
        np.ndarray
            Rotated B matrix
        """
        rotation = self.rotation_matrix
        b_matrix = self.b_matrix
        if not (rotation is None or b_matrix is None):
            b_matrix = np.dot(rotation.T, np.dot(b_matrix, rotation))
            return nearest_pos_semi_def(b_matrix)

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
    def rotation_matrix(self) -> np.array:
        """
        Returns the rotation matrix between array indices and mm.

        See Also
        --------
        * :func:`get_rotation_matrix`

        Returns
        -------
        np.array
            Rotation matrix
        """
        return self.get_rotation_matrix()

    @property
    def spatial_resolution(self) -> Tuple[float]:
        """
        Returns the spatial resolution of the image in millimeters.

        See Also
        --------
        * :func:`get_spatial_resolution`

        Returns
        -------
        Tuple[float]
            Spatial resolution in millimeters
        """
        return self.get_spatial_resolution()

    @property
    def affine(self) -> np.array:
        """
        Returns the affine transformation of this image.

        See Also
        --------
        * :func:`get_affine`

        Returns
        -------
        np.array
            Affine transformation matrix
        """
        return self.get_affine()

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
        """
        Returns the default relative path for this image within a DICOM
        archive.

        See Also
        --------
        * :func:`get_default_relative_path`

        Returns
        -------
        Path
            Default relative path for this image
        """
        return self.get_default_relative_path()

    @property
    def b_matrix(self) -> np.ndarray:
        """
        Returns the B matrix of Siemens scans.

        See Also
        --------
        :func:`~dicom_parser.utils.siemens.private_tags.parse_siemens_b_matrix`
        :func:`get_b_matrix`

        Returns
        -------
        np.ndarray
            B matrix
        """
        return self.get_b_matrix()

    @property
    def q_vector(self) -> np.ndarray:
        """
        Calculates Siemens DWI q-vector in voxel space.

        See Also
        --------
        * :func:`~dicom_parser.utils.siemens.private_tags.b_matrix_to_q_vector`
        * :func:`get_q_vector`

        Returns
        -------
        np.ndarray
            q-vector
        """
        return self.get_q_vector()

    @property
    def voxel_space_b_matrix(self) -> np.ndarray:
        """
        Returns the B matrix in voxel space (rather than patient space).

        See Also
        --------
        * :func:`voxel_space_b_matrix`

        Returns
        -------
        np.ndarray
            Rotated B matrix
        """
        return self.get_voxel_space_b_matrix()
