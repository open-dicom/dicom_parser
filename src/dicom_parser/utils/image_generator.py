"""
Definition of the :func:`generate_images` utility function.
"""
from pathlib import Path
from typing import Iterable, Optional

from dicom_parser.image import Image
from dicom_parser.utils.path_generator import generate_paths

#: An iterable of extensions to be included by default.
DEFAULT_EXTENSIONS = (".dcm", ".ima")


def generate_images(
    path: Path,
    extension: Optional[Iterable[str]] = DEFAULT_EXTENSIONS,
    mime: bool = False,
    allow_empty: bool = False,
) -> Iterable[Image]:
    """
    Returns a tuple of :class:`~dicom_parser.image.Image` instances
    ordered by instance number.

    Parameters
    ----------
    path : Path
        Root directory to generate files from
    extension : Iterable[str], optional
        Extensions to filter files in parent directory by
    mime : bool, optional
        Whether to find DICOM images by file mime type instead of
        extension, defaults to False
    allow_empty : bool, optional
        Whether to not raise a FileNotFoundError if no images are detected, by
        default False

    Returns
    -------
    Iterable[Image]
        Image instances generator
    """
    return (
        Image(dcm_path)
        for dcm_path in generate_paths(
            path,
            mime=mime,
            extension=extension,
            allow_empty=allow_empty,
        )
    )
