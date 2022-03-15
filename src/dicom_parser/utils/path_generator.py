"""
Definition of the :func:`generate_paths` utility function.
"""
from pathlib import Path
from typing import Iterable, Optional

from dicom_parser.utils import messages
from dicom_parser.utils.mime_generator import generate_by_mime
from dicom_parser.utils.peek import peek


def format_empty_exception(
    path: Path,
    extension: Optional[Iterable[str]] = None,
    mime: bool = False,
) -> str:
    if mime:
        return messages.EMPTY_BY_MIME.format(path=path)
    elif extension is not None:
        return messages.EMPTY_BY_EXTENSION.format(
            path=path, extension=extension
        )
    else:
        return messages.EMPTY_DIRECTORY.format(path=path)


def generate_paths(
    path: Path,
    extension: Optional[Iterable[str]] = None,
    mime: bool = False,
    allow_empty: bool = False,
) -> Iterable[Path]:
    """
    Generates file paths filtered by *extension* or *mime* type.

    Note
    ----
    When using *mime*, all files are inspected and *extension* is ignored.

    Parameters
    ----------
    path : Path
        Root directory to generate files from
    extension : Optional[Iterable[str]], optional
        Extensions to filter files by
    mime : bool, optional
        Whether to return files by mime type (instead of extension), by
        default False
    allow_empty : bool, optional
        Whether to not raise a FileNotFoundError if no matching files exist, by
        default False

    Returns
    -------
    Iterable[Path]
        Matching paths

    Raises
    ------
    FileNotFoundError
        No matching files detected in the specified path
    """
    if mime:
        matches = generate_by_mime(path)
    elif extension is not None:
        matches = (
            p
            for p in path.rglob("*")
            if p.is_file() and p.suffix.lower() in extension
        )
    else:
        matches = path.rglob("*")
    if not allow_empty:
        # Use peek to convert matches to None if the generator is "empty"
        _, matches = peek(matches)
        if not matches:
            message = format_empty_exception(
                path, extension=extension, mime=mime
            )
            raise FileNotFoundError(message)
    return matches
