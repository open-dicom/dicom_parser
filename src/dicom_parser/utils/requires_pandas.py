from collections.abc import Callable

try:
    # pylint: disable=unused-import
    import pandas as pd  # noqa: F401; lgtm [py/unused-import]
except ImportError:
    _has_pandas = False
else:
    _has_pandas = True


REQUIRES_PANDAS: str = """Pandas could not be imported!
Please install pandas by running:

pip install dicom_parser[pandas]
"""


def requires_pandas(func: Callable) -> Callable:
    def check_pandas(*args, **kwargs):
        if not _has_pandas:
            raise ImportError(REQUIRES_PANDAS)
        return func(*args, **kwargs)

    return check_pandas
