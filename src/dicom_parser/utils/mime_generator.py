"""
Definition of the :func:`generate_by_mime` utility function.
For more information about mime types see `this SO answer`_ or `this MDN
article`_.

.. _this SO answer:
   https://stackoverflow.com/a/3828381/4416932
.. _this MDN article:
   https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types
"""
import platform
from pathlib import Path
from typing import Generator

from dicom_parser.utils.messages import MUGGLES, WINDOWS

#: DICOM file's expected mime type.
DICOM_MIME_TYPE = "application/dicom"


def check_magic() -> None:
    """
    Checks whether python-magic is available.

    Raises
    ------
    NotImplementedError
        Generation by mime type is not supported on Windows
    ImportError
        Dependency not installed
    """
    if platform.system() == "Windows":
        raise NotImplementedError(WINDOWS)
    try:
        # pylint: disable=unused-import
        import magic  # noqa: F401
    except ModuleNotFoundError:
        raise ImportError(MUGGLES)


def generate_by_mime(
    root_path: Path, pattern: str = "*", mime_type: str = DICOM_MIME_TYPE
) -> Generator:
    """
    Wrapper around the :func:`_generate_by_mime` generator function.

    Note
    ----
    This wrapper is required in order to execute :func:`check_magic` before
    the iteration itself.

    Parameters
    ----------
    root_path : Path
        Base directory path to recursively iterate
    pattern : str, optional
        The glob pattern used to iterate files, by default "*"
    mime_type : str, optional
        Desired file mime type, by default DICOM_MIME_TYPE

    Yields
    -------
    GeneratorType
        Paths of the desired mime type
    """
    check_magic()
    return _generate_by_mime(root_path, pattern, mime_type)


def _generate_by_mime(
    root_path: Path, pattern: str = "*", mime_type: str = DICOM_MIME_TYPE
) -> Generator:
    """
    Yields files with the provided *mime_type*.

    Parameters
    ----------
    root_path : Path
        Base directory path to recursively iterate
    pattern : str, optional
        The glob pattern used to iterate files, by default "*"
    mime_type : str, optional
        Desired file mime type, by default DICOM_MIME_TYPE

    Yields
    -------
    GeneratorType
        Paths of the desired mime type
    """
    import magic

    for path in Path(root_path).rglob(pattern):
        try:
            path_mime = magic.from_file(str(path), mime=True)
        except IsADirectoryError:
            continue
        else:
            if path_mime == mime_type:
                yield path
