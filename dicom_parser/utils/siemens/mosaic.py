"""
Defines the :class:`~dicom_parser.utils.siemens.mosaic.Mosaic` class
that decodes the 2D encoding of 3D volumes used by Siemens.
For more information read `this <https://nipy.org/nibabel/dicom/dicom_mosaic.html>`_
`NiBabel <https://nipy.org/nibabel/index.html>`_ article or see pages 10-12 in
`here <https://discovery.ucl.ac.uk/id/eprint/1495621/1/Li%20et%20al%20The%20first%20step%20for%20neuroimaging%20data%20analysis%20-%20DICOM%20to%20NIfTI%20conversion.pdf>`_.

"""

import numpy as np

from dicom_parser.header import Header


class Mosaic:
    """
    A Siemens mosaic of 2D images representing a single volume.

    """

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
        self.series_header_info = self.header.get("CSASeriesHeaderInfo")
        self.volume_shape = self.get_volume_shape()
        self.mosaic_dimensions = self.get_mosaic_dimensions()
        self.ascending = "Asc" in self.series_header_info["SliceArray"]

    def get_volume_shape(self) -> tuple:
        """
        Returns the dimensions of the volume that will be created.

        Returns
        -------
        tuple
            x_dim, y_dim, z_dim
        """

        acquisition_matrix = self.header.get("AcquisitionMatrix")
        x, y = acquisition_matrix[0], acquisition_matrix[-1]
        z = self.series_header_info["SliceArray"]["Size"]
        return x, y, z

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
