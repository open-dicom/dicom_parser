"""
Vendor specific private tags they may not be accessible by keyword using pydicom.

"""


# Based on `this <https://nipy.org/nibabel/dicom/siemens_csa.html>`_ article.
SIEMENS_PRIVATE_TAGS = {
    "CSAImageHeaderType": ("0029", "1008"),
    "CSAImageHeaderVersion": ("0029", "1009"),
    "CSAImageHeaderInfo": ("0029", "1010"),
    "CSASeriesHeaderType": ("0029", "1018"),
    "CSASeriesHeaderVersion": ("0029", "1019"),
    "CSASeriesHeaderInfo": ("0029", "1020"),
}
