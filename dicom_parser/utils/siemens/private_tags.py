"""
Siemens specific private tags they may not be accessible by keyword using
`pydicom <https://github.com/pydicom/pydicom>`_.

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

CSA_FLAG_TAG = "0029", "1009"
NUMBER_OF_IMAGES_IN_MOSAIC_TAG = "0019", "100a"
