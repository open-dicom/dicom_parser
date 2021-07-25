"""
Definition of the :func:`format_header_df` utility function, used to display
a formatted version of a single DICOM header's information dataframe.
"""
import functools

from dicom_parser.utils import requires_pandas


@requires_pandas
def format_header_df(df, max_colwidth: int = 28) -> str:
    """
    Formats a raw DICOM header's dataframe to display the contained information
    more conveniently.

    Parameters
    ----------
    df : pd.DataFrame
        Raw header information
    max_colwidth : int, optional
        Maximal column width for formatted table, by default 28

    Returns
    -------
    str
        Formatted dataframe information
    """
    if df is None:
        return ""
    formatters = {}
    for column_name in df.columns:
        form = None
        if column_name in ("Keyword", "Value"):
            # Convert to string, left-align, and truncate at MAX_COL_WIDTH - 1
            form = "{{!s:<{}}}".format(max_colwidth - 1)
        elif column_name == "VR":
            # Set column width to longest VR value and left-align
            max_length = df[column_name].str.len().max()
            form = "{{:<{}}}".format(max_length)
        elif column_name in ("VM", "Index"):
            # Left-align and set column width to 2
            form = "{{:<2}}".format()
        if form is not None:
            formatters[column_name] = functools.partial(str.format, form)
    return df.to_string(
        formatters=formatters, justify="left", max_colwidth=max_colwidth
    )
