import numpy as np


def none_or_close(val1, val2, rtol=1e-5, atol=1e-6):
    """
    Match if `val1` and `val2` are both None, or are close.

    Parameters
    ----------
    val1 : None or array-like
    val2 : None or array-like
    rtol : float, optional
       Relative tolerance; see ``np.allclose``
    atol : float, optional
       Absolute tolerance; see ``np.allclose``

    Returns
    -------
    tf : bool
       True iff (both `val1` and `val2` are None) or (`val1` and `val2`
       are close arrays, as detected by ``np.allclose`` with parameters
       `rtol` and `atal`).

    References
    ----------
    * `nicom's implementation`_

    .. _nicom's implementation:
       https://github.com/nipy/nibabel/blob/62aea04248e70d7c4529954ca41685d7f75a0b1e/nibabel/nicom/dicomwrappers.py#L950

    Examples
    --------
    >>> none_or_close(None, None)
    True
    >>> none_or_close(1, None)
    False
    >>> none_or_close(None, 1)
    False
    >>> none_or_close([1,2], [1,2])
    True
    >>> none_or_close([0,1], [0,2])
    False
    """
    if val1 is None and val2 is None:
        return True
    if val1 is None or val2 is None:
        return False
    return np.allclose(val1, val2, rtol, atol)
