"""
Definition of the :class:`Mosaic` class that decodes the 2D encoding of 3D
volumes used by Siemens. For more information read `this
<https://nipy.org/nibabel/dicom/dicom_mosaic.html>`_ `NiBabel
<https://nipy.org/nibabel/index.html>`_ article or see pages 10-12 in
`here
<https://discovery.ucl.ac.uk/id/eprint/1495621/1/Li%20et%20al%20The%20first%20step%20for%20neuroimaging%20data%20analysis%20-%20DICOM%20to%20NIfTI%20conversion.pdf>`_.
"""
from typing import Tuple

import numpy as np
from dicom_parser.header import Header
from dicom_parser.utils.siemens import messages


class Mosaic:
    """
    A Siemens mosaic of 2D images representing a single volume.
    """

    CSA_ASCII_HEADER_KEY: str = "MrPhoenixProtocol"
    CSA_ASCII_SLICE_ARRAY_KEY: str = "sSliceArray"
    CSA_SERIES_INFO_KEY: str = "CSASeriesHeaderInfo"

    def __init__(self, mosaic_array: np.ndarray, header: Header):
        """
        Reads required attributes from the header and parses out the
        dimensions of both the mosaic and the encoded volume.

        Parameters
        ----------
        mosaic_array : np.ndarray
            Mosaic of 2D images
        header : Header
            The image's header information
        """
        self.mosaic_array = mosaic_array
        self.header = header

        # Read series CSA header (contains information about the mosaic
        # dimensions).
        self.series_header_info = self.header.get(self.CSA_SERIES_INFO_KEY)

        # Number of images encoded in the mosaic.
        self.n_images = self.get_n_images()

        # Number of rows and columns that make up the mosaic.
        self.size = int(np.ceil(np.sqrt(self.n_images)))

        # Read the ASCII (ASCCONV) header encoded withing the series CSA
        # header.
        self.ascii_header = self.series_header_info.get(
            self.CSA_ASCII_HEADER_KEY, {}
        ).get("value", {})
        self.slice_array = self.ascii_header.get(
            self.CSA_ASCII_SLICE_ARRAY_KEY, {}
        )
        self.ascending = "anAsc" in self.slice_array
        self.volume_shape = self.get_volume_shape()
        self.mosaic_dimensions = self.get_mosaic_dimensions()

    def get_n_images(self) -> int:
        """
        Returns the number of images encoded in the mosaic.

        Returns
        -------
        int
            Number of images encoded in mosaic
        """
        try:
            return self.header["NumberOfImagesInMosaic"]
        except KeyError:
            raise KeyError(messages.MISSING_NUMBER_OF_IMAGES)

    def get_image_shape(self) -> Tuple[int, int]:
        """
        Returns the 2D shape of a single image within the mosaic.

        Returns
        -------
        Tuple[int, int]
            Single image shape
        """
        x = self.header.get("Rows")
        y = self.header.get("Columns")
        if x is not None and y is not None:
            return (x // self.size, y // self.size)

    def get_volume_shape(self) -> Tuple[float, float, float]:
        """
        Returns the dimensions of the volume that will be created.

        Returns
        -------
        Tuple[float, float, float]
            Volume shape
        """
        image_shape = self.get_image_shape()
        if image_shape is not None:
            z = self.slice_array.get("lSize", 0)
            return (*image_shape, z)

    def get_image_position(
        self, iop: np.ndarray
    ) -> Tuple[float, float, float]:
        """
        Returns a fixed Image Position (Patient) header field value.

        Parameters
        ----------
        iop : np.ndarray
            Image Orientation (Patient) header field value

        References
        ----------
        * https://nipy.org/nibabel/dicom/dicom_mosaic.html

        Returns
        -------
        Tuple[float, float, float]
            Image Position (Patient) header field value
        """
        try:
            x = self.header["Rows"]
            y = self.header["Columns"]
            raw_ipp = self.header["ImagePositionPatient"]
            pixel_spacing = self.header["PixelSpacing"]
        except KeyError:
            return
        raw_shape = np.array([x, y])

        slice_shape = raw_shape / self.size
        translation_fix = (raw_shape - slice_shape) / 2
        Q = np.fliplr(iop) * pixel_spacing
        return raw_ipp + np.dot(Q, translation_fix[:, None]).ravel()

    def get_mosaic_dimensions(self) -> tuple:
        """
        Returns the number of rows and columns that make up the mosaic.

        Returns
        -------
        tuple
            n_rows, n_columns
        """
        n_rows = self.header.get("Rows") // self.volume_shape[0]
        n_columns = self.header.get("Columns") // self.volume_shape[1]
        return n_rows, n_columns

    def get_tile(self, i_row: int, i_column: int) -> np.ndarray:
        """
        Cut out a tile of the mosaic by row and column indices.

        Parameters
        ----------
        i_row : int
            Row index
        i_column : int
            Column index

        Returns
        -------
        np.ndarray
            A single tile at the (i_row, i_column) position
        """
        x_start = self.volume_shape[0] * i_row
        x_end = self.volume_shape[0] * (i_row + 1)
        y_start = self.volume_shape[1] * i_column
        y_end = self.volume_shape[1] * (i_column + 1)
        return self.mosaic_array[x_start:x_end, y_start:y_end]

    def get_tiles(self) -> list:
        """
        Cuts out the tiles (2D slices) from the mosaic.

        Returns
        -------
        list
            Tiles collected by row
        """
        n_rows = self.mosaic_dimensions[0]
        n_columns = self.mosaic_dimensions[1]
        return [
            self.get_tile(i_row, i_column)
            for i_row in range(n_rows)
            for i_column in range(n_columns)
        ]

    def tiles_to_volume(self, tiles: list) -> np.ndarray:
        """
        Transforms a list of tiles to a correctly oriented volume.

        Parameters
        ----------
        tiles : list
            List of 2D slices as parsed from the mosaic

        Returns
        -------
        np.ndarray
            Orientation-fixed volume
        """
        if not self.ascending:
            tiles = tiles[::-1]
        volume = np.stack(tiles, axis=-1).transpose((1, 0, 2))
        return np.flip(volume, axis=1)

    def fold(self) -> np.ndarray:
        """
        Folds the 2D mosaic to become a 3D volume.

        Returns
        -------
        np.ndarray
            3D volume
        """
        tiles = self.get_tiles()
        return self.tiles_to_volume(tiles)
