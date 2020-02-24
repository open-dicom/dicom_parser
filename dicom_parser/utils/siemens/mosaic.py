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
        self.series_header_info = self.header.get_csa("CSASeriesHeaderInfo")
        self.volume_shape = self.get_volume_shape()
        self.mosaic_dimensions = self.get_mosaic_dimensions()
        self.ascending = "Asc" in self.series_header_info.parsed["SliceArray"]

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
        z = self.series_header_info.n_slices
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

    def fold(self) -> np.ndarray:
        """
        Folds the 2D mosaic to become a 3D volume.

        Returns
        -------
        np.ndarray
            3D volume
        """

        n_rows = self.mosaic_dimensions[0]
        n_columns = self.mosaic_dimensions[1]
        slices = [
            self.get_tile(i_row, i_column)
            for i_row in range(n_rows)
            for i_column in range(n_columns)
        ]
        if not self.ascending:
            return np.stack(slices[::-1])
        return np.stack(slices)
