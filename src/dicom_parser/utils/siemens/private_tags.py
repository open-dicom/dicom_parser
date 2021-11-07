"""
Siemens specific private tags they may not be accessible by keyword using
`pydicom <https://github.com/pydicom/pydicom>`_.
"""
import array

import numpy as np
from dicom_parser.utils.siemens import messages
from dicom_parser.utils.siemens.csa.header import CsaHeader

#: The raw (6, 1) vector returned represents the upper triangle of a symmetric
#: B matrix.
B_MATRIX_INDICES = np.array([0, 1, 2, 1, 3, 4, 2, 4, 5])


def parse_siemens_slice_timing(value: bytes) -> list:
    """
    Parses a SIEMENS MR image's slice timing as saved in the private
    (0019, 1029) `MosaicRefAcqTimes`_ tag to a list of floats representing
    slice times in milliseconds.

    .. _MosaicRefAcqTimes:
       https://en.wikibooks.org/wiki/SPM/Slice_Timing#Siemens_scanners

    Parameters
    ----------
    value : bytes
        SIEMENS private MosaicRefAcqTimes data element

    Returns
    -------
    list
        Slice times in milliseconds
    """
    return [
        round(slice_time, 5) for slice_time in list(array.array("d", value))
    ]


def parse_siemens_gradient_direction(value: bytes) -> list:
    """
    Parses a SIEMENS MR image's B-vector as represented in the private
    (0019, 100E) `DiffusionGradientDirection`_ DICOM tag.

    .. _DiffusionGradientDirection:
       https://na-mic.org/wiki/NAMIC_Wiki:DTI:DICOM_for_DWI_and_DTI#Private_vendor:_Siemens

    Parameters
    ----------
    value : bytes
        SIEMENS private DiffusionGradientDirection data element.

    Returns
    -------
    list
        Gradient directions (B-vector)
    """
    return [float(value) for value in list(array.array("d", value))]


def parse_siemens_number_of_slices_in_mosaic(value: bytes) -> int:
    return int.from_bytes(value, byteorder="little")


def parse_siemens_b_matrix(value: bytes) -> np.ndarray:
    """
    Parses the Siemens B matrix header field value.

    Parameters
    ----------
    value : bytes
        Raw B matrix header field value

    Returns
    -------
    np.ndarray
        Parsed B matrix
    """
    raw = list(array.array("d", value))
    return np.array(raw)[B_MATRIX_INDICES].reshape(3, 3)


def b_matrix_to_q_vector(
    b_matrix: np.ndarray, tol: float = None
) -> np.ndarray:
    """
    Estimate q-vector from B matrix.

    References
    ----------
    * https://github.com/nipy/nibabel/blob/ea68c4ecf914e9b0486b2b01c72fce345ba186fb/nibabel/nicom/dwiparams.py#L26

    Parameters
    ----------
    b_matrix : np.ndarray (3, 3)
        B matrix

    Returns
    -------
    np.ndarray
        q-vector
    """
    if b_matrix is None:
        return None
    is_symmetric = np.allclose(b_matrix, b_matrix.T)
    if not is_symmetric:
        message = messages.B_MATRIX_NOT_SYMMETRIC.format(b_matrix=b_matrix)
        raise ValueError(message)
    w, v = np.linalg.eigh(b_matrix)
    if tol is None:
        tol = np.abs(w.max()) * b_matrix.shape[0] * np.finfo(w.dtype).eps
    non_trivial = np.abs(w) > tol
    if np.any(w[non_trivial] < 0):
        message = messages.INVALID_B_MATRIX.format(b_matrix=b_matrix)
        raise ValueError(message)
    inds = np.argsort(w)[::-1]
    max_ind = inds[0]
    vector = v[:, max_ind]
    # because the factor is a sqrt, the sign of the vector is arbitrary.
    # We arbitrarily set it to have a positive x value.
    if vector[0] < 0:
        vector *= -1
    return vector * w[max_ind]


def nearest_pos_semi_def(b_matrix: np.ndarray):
    """
    Least squares positive semi-definite tensor estimation.

    References
    ----------
    * Niethammer M, San Jose Estepar R, Bouix S, Shenton M,
      Westin CF.  On diffusion tensor estimation. Conf Proc IEEE Eng Med
      Biol Soc.  2006;1:2622-5. PubMed PMID: 17946125; PubMed Central
      PMCID: PMC2791793.
    * https://github.com/nipy/nibabel/blob/ea68c4ecf914e9b0486b2b01c72fce345ba186fb/nibabel/nicom/dwiparams.py#L70

    Parameters
    ----------
    b_matrix : np.ndrray
       B matrix

    Returns
    -------
    npds : (3,3) array
       Estimated nearest positive semi-definite array to matrix `B`

    Examples
    --------
    >>> B = np.diag([1, 1, -1])
    >>> nearest_pos_semi_def(B)
    array([[0.75, 0.  , 0.  ],
           [0.  , 0.75, 0.  ],
           [0.  , 0.  , 0.  ]])
    """
    B = np.asarray(b_matrix)
    vals, vecs = np.linalg.eigh(B)
    # indices of eigenvalues in descending order
    inds = np.argsort(vals)[::-1]
    vals = vals[inds]
    cardneg = np.sum(vals < 0)
    if cardneg == 0:
        return B
    if cardneg == 3:
        return np.zeros((3, 3))
    lam1a, lam2a, lam3a = vals
    scalers = np.zeros((3,))
    if cardneg == 2:
        b112 = np.max([0, lam1a + (lam2a + lam3a) / 3.0])
        scalers[0] = b112
    elif cardneg == 1:
        lam1b = lam1a + 0.25 * lam3a
        lam2b = lam2a + 0.25 * lam3a
        if lam1b >= 0 and lam2b >= 0:
            scalers[:2] = lam1b, lam2b
        else:  # one of the lam1b, lam2b is < 0
            if lam2b < 0:
                b111 = np.max([0, lam1a + (lam2a + lam3a) / 3.0])
                scalers[0] = b111
            if lam1b < 0:
                b221 = np.max([0, lam2a + (lam1a + lam3a) / 3.0])
                scalers[1] = b221
    # resort the scalers to match the original vecs
    scalers = scalers[np.argsort(inds)]
    return np.dot(vecs, np.dot(np.diag(scalers), vecs.T))


def parse_siemens_bandwith_per_pixel_phase_encode(value: bytes):
    return array.array("d", value)[0]


def parse_siemens_csa_header(value: bytes) -> dict:
    return CsaHeader(value).read()


SIEMENS_PRIVATE_TAGS = {
    # Csa Headers
    # See: https://nipy.org/nibabel/dicom/siemens_csa.html.
    "CSAImageHeaderType": ("0029", "1008"),
    "CSAImageHeaderVersion": ("0029", "1009"),
    "CSAImageHeaderInfo": ("0029", "1010"),
    "CSASeriesHeaderType": ("0029", "1018"),
    "CSASeriesHeaderVersion": ("0029", "1019"),
    "CSASeriesHeaderInfo": ("0029", "1020"),
    # DTI
    # https://na-mic.org/wiki/NAMIC_Wiki:DTI:DICOM_for_DWI_and_DTI
    "NumberOfImagesInMosaic": ("0019", "100a"),
    "SliceMeasurementDuration": ("0019", "100b"),
    "DiffusionDirectionality": ("0019", "100d"),
    "DiffusionGradientDirection": ("0019", "100e"),
    "GradientMode": ("0019", "100f"),
    "B_value": ("0019", "100c"),
    "B_matrix": ("0019", "1027"),
    "BandwidthPerPixelPhaseEncode": ("0019", "1028"),
    "MosaicRefAcqTimes": ("0019", "1029"),
}
