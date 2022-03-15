"""
Definition of the :class:`Series` class.
"""
from pathlib import Path
from typing import Any, Iterable, Optional, Tuple

import numpy as np

from dicom_parser import messages
from dicom_parser.image import Image
from dicom_parser.messages import (
    INVALID_INDEXING_OPERATOR,
    INVALID_SERIES_DIRECTORY,
)
from dicom_parser.utils.image_generator import generate_images

DEFAULT_EXTENSIONS = (".dcm", ".ima")


class Series:
    """
    This class represents a complete collection of Image instances originating
    from a single directory and ordered by InstanceNumber.
    """

    def __init__(
        self,
        path: Optional[Path] = None,
        images: Optional[Iterable[Image]] = None,
        extension: Optional[Iterable[str]] = DEFAULT_EXTENSIONS,
        mime: bool = False,
    ):
        """
        The Series class should be initialized with a string or a
        :class:`~pathlib.Path` instance representing the path of single
        `DICOM series`_, or an iterable or :class:`dicom_parser.image.Image`
        instances (one of *path* or *images* must be provided).

        .. _DICOM series:
           https://dcm4che.atlassian.net/wiki/spaces/d2/pages/1835038/A+Very+Basic+DICOM+Introduction

        Parameters
        ----------
        path : :class:`~pathlib.Path` or str, optional
            Directory containing stored DICOM images
        images : Iterable[Image], optional
            Image instances that make up the series
        extension : Iterable[str], optional
            Extensions to filter files in parent directory by
        mime : bool, optional
            Whether to find DICOM images by file mime type instead of
            extension, defaults to False
        """
        # Find images in series directory path, if provided.
        if isinstance(path, (Path, str)):
            self.path = self.check_path(path)
            self.images = self.get_images(mime=mime, extension=extension)
        # Tupelize any iterable of images.
        elif images is not None:
            self.images = tuple(images)
        # Otherwise, raise an exception.
        else:
            raise ValueError(messages.MISSING_SERIES_SOURCE)

        # Pixel array cache.
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
        Provide dictionary-like indexing-operator functionality for querying
        header information using a str or a tuple, and list-like functionality
        for int, returning the image at the given index.

        Parameters
        ----------
        key : str or tuple or int
            The key or tag for which to retrieve header information,
            or the index for the required :class:`~dicom_parser.image.Image`
            instance

        Returns
        -------
        type
            Parsed header information of the given key or the image at the
            given index
        """
        if isinstance(key, (str, tuple)):
            return self.get(key, missing_ok=False)
        elif isinstance(key, (int, slice)) and not isinstance(key, bool):
            return self.images[key]
        else:
            message = INVALID_INDEXING_OPERATOR.format(key=key)
            raise TypeError(message)

    @staticmethod
    def check_path(path) -> Path:
        """
        Converts to a :class:`~pathlib.Path` instance if required and checks
        that it represents an existing directory.

        Parameters
        ----------
        path : str or Path
            The provided path.

        Returns
        -------
        Path
            A pathlib.Path instance representing an existing directory

        Raises
        ------
        ValueError
            If the provided path is not an existing directory
        """
        path = Path(path)
        if not path.is_dir():
            message = INVALID_SERIES_DIRECTORY.format(path=path)
            raise ValueError(message)
        return path

    def get_images(
        self,
        mime: bool = False,
        extension: Optional[Iterable[str]] = DEFAULT_EXTENSIONS,
    ) -> tuple:
        """
        Returns a tuple of :class:`~dicom_parser.image.Image` instances
        ordered by instance number.

        Returns
        -------
        tuple
            Image instance by instance number
        mime : bool, optional
            Whether to find DICOM images by file mime type instead of
            extension, defaults to False
        extension : Iterable[str], optional
            Extensions to filter files in parent directory by
        """
        images = generate_images(
            self.path, extension=extension, mime=mime, allow_empty=False
        )
        return tuple(
            sorted(
                images, key=lambda image: image.header.get("InstanceNumber")
            )
        )

    def get(
        self,
        tag_or_keyword,
        default=None,
        parsed: bool = True,
        missing_ok: bool = True,
    ) -> Any:
        """
        Returns header information from the
        :class:`~dicom_parser.image.Image` instances that compose this series.
        If one distinct value is returned from all the images' headers,
        returns that value. Otherwise, returns a list of the values
        (ordered the same as the `images` attribute, by instance number).

        Parameters
        ----------
        tag_or_keyword : tuple or str, or list
            Tag or keyword representing the requested data element, or a list
            of such
        default : Any, optional
            Default value to be returned if the key doesn't exist, default is
            None
        parsed : bool, optional
            Whether to return a parsed or raw value (the default is True,
            which will return the parsed value)
        missing_ok : bool, optional
            Whether to treat missing key as None (otherwise, raises an
            exception), default is True

        Returns
        -------
        Any
            The requested data element value for the entire series
        """
        values = [
            image.header.get(
                tag_or_keyword,
                default=default,
                parsed=parsed,
                missing_ok=missing_ok,
            )
            for image in self.images
        ]
        unique_values = set(values)
        return values if len(unique_values) > 1 else unique_values.pop()

    def get_spatial_resolution(self) -> Tuple[float]:
        """
        Returns the spatial resolution of the series in millimeters.

        Returns
        -------
        Tuple[float]
            Spatial resolution in millimeters
        """
        return self.images[0].spatial_resolution

    def get_bids_path(self) -> str:
        """
        Build BIDS-appropriate path for the series.
        Returns
        -------
        str
            BIDS-appropriate path
        """
        return self.images[0].get_bids_path()

    @property
    def bids_path(self) -> str:
        """
        Builds BIDS-appropriate path according to DICOM's header
        Returns
        -------
        str
            BIDS-appropriate path
        """
        return self.get_bids_path()

    @property
    def data(self) -> np.ndarray:
        """
        Caches the stacked 3D array containing the entire series' data.

        Returns
        -------
        np.ndarray
            Series 3D data
        """
        if not isinstance(self._data, np.ndarray):
            self._data = np.stack(
                [image.data for image in self.images], axis=-1
            )
        return self._data

    @property
    def spatial_resolution(self) -> tuple:
        """
        Returns the spatial resolution of the series.

        Returns
        -------
        tuple
            Spatial resolution
        """
        return self.get_spatial_resolution()
