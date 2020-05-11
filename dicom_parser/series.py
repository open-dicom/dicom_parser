"""
Definition of the Series class, representing a collection of Image instances
ordered by the header's InstanceNumber data element.

"""

import numpy as np

from dicom_parser.image import Image
from dicom_parser.utils.peek import peek
from pathlib import Path
from types import GeneratorType


class Series:
    """
    This class represents a complete collection of Image instances originating from
    a single directory and ordered by InstanceNumber.

    """

    def __init__(self, path: Path):
        """
        The Series class should be initialized with a string or a :class:`~pathlib.Path`
        instance representing the path of single
        `DICOM series <https://dcm4che.atlassian.net/wiki/spaces/d2/pages/1835038/A+Very+Basic+DICOM+Introduction>`_.

        Parameters
        ----------
        path : :class:`~pathlib.Path` or str
            Directory containing .dcm files.
        """

        self.path = self.check_path(path)
        self.images = self.get_images()
        self._data = None

    def __len__(self) -> int:
        """
        Returns the number of images this Series instance is composed of.

        Returns
        -------
        int
            Number of DICOM images in this series.
        """

        return len(self.images)

    def __getitem__(self, key):
        """
        Provide dictionary-like indexing-operator functionality for querying header
        information using a str or a tuple, and list-like functionality for int,
        returning the image at the given index.

        Parameters
        ----------
        key : str or tuple or int
            The key or tag for which to retrieve header information,
            or the index for the required :class:`~dicom_parser.image.Image` instance.

        Returns
        -------
        type
            Parsed header information of the given key or the image at the given index.
        """

        if isinstance(key, (str, tuple)):
            return self.get(key, missing_ok=False)
        elif isinstance(key, (int, slice)) and not isinstance(key, bool):
            return self.images[key]
        else:
            raise TypeError(
                f"Invalid indexing operator value ({key})! Must be of type str, tuple, int, or slice."
            )

    def check_path(self, path) -> Path:
        """
        Converts to a :class:`~pathlib.Path` instance if required and checks that it
        represents an existing directory.

        Parameters
        ----------
        path : str or Path
            The provided path.

        Returns
        -------
        Path
            A pathlib.Path instance representing an existing directory.

        Raises
        ------
        ValueError
            If the provided path is not an existing directory.
        """

        path = Path(path)
        if not path.is_dir():
            raise ValueError(
                f"Series instances must be initialized with a valid directory path! Could not locate directory {path}."
            )
        return path

    def get_dcm_paths(self) -> GeneratorType:
        """
        Returns a generator of .dcm files within the provided directory path.

        Returns
        -------
        GeneratorType
            DICOM images (.dcm files) generator.

        Raises
        ------
        FileNotFoundError
            No DICOM images found under provided directory.
        """

        _, dcm_paths = peek(self.path.rglob("*.dcm"))
        if not dcm_paths:
            raise FileNotFoundError(
                "Could not locate any .dcm files within the provided series directory!"
            )
        return dcm_paths

    def get_images(self) -> tuple:
        """
        Returns a tuple of :class:`~dicom_parser.image.Image` instances
        ordered by instance number.

        Returns
        -------
        tuple
            Image instance by instance number.
        """

        images = [Image(dcm_path) for dcm_path in self.get_dcm_paths()]
        return tuple(
            sorted(images, key=lambda image: image.header.get("InstanceNumber"))
        )

    def get(
        self, tag_or_keyword, default=None, parsed: bool = True, missing_ok: bool = True
    ):
        """
        Returns header information from the
        :class:`~dicom_parser.image.Image` that compose this series.
        If one distinct value is returned from all the images' headers,
        returns that value. Otherwise, returns a list of the values
        (ordered the same as the `images` attribute, by instance number).

        Parameters
        ----------
        tag_or_keyword : tuple or str, or list
            Tag or keyword representing the requested data element, or a list of such.

        Returns
        -------
        type
            The requested data element value for the entire series
        """

        values = [
            image.header.get(
                tag_or_keyword, default=default, parsed=parsed, missing_ok=missing_ok
            )
            for image in self.images
        ]
        unique_values = set(values)
        return values if len(unique_values) > 1 else unique_values.pop()

    def get_spatial_resolution(self) -> tuple:
        sample_header = self.images[0]
        pixel_spacing = sample_header.get("PixelSpacing")
        slice_thickness = sample_header.get("SliceThickness")
        if slice_thickness:
            return tuple(pixel_spacing.append(slice_thickness))
        else:
            return tuple(pixel_spacing)

    @property
    def data(self) -> np.ndarray:
        """
        Caches the stacked 3D array containing the entire series' data.

        Returns
        -------
        np.ndarray
            Series 3D data.
        """

        if not isinstance(self._data, np.ndarray):
            self._data = np.stack([image.data for image in self.images], axis=-1)
        return self._data

    @property
    def spatial_resolution(self) -> tuple:
        return self.get_spatial_resolution()
