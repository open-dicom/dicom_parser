import numpy as np

from dicom_parser.image import Image
from dicom_parser.utils.peek import peek
from pathlib import Path
from types import GeneratorType


class Series:
    def __init__(self, path: Path):
        self.path = self.check_path(path)
        self.images = self.get_images()
        self._data = None

    def check_path(self, path) -> Path:
        """
        Checks that the path if a :class:`~pathlib.Path` instance and that
        it represents an existing directory.
        
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
