"""
Siemens specific private tags they may not be accessible by keyword using
`pydicom <https://github.com/pydicom/pydicom>`_.

"""


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
    "B_value": ("0019", "100c"),
    "DiffusionDirectionality": ("0019", "100d"),
    "DiffusionGradientDirection": ("0019", "100e"),
    "GradientMode": ("0019", "100f"),
    "B_matrix": ("0019", "1027"),
    "BandwidthPerPixelPhaseEncode": ("0019", "1028"),
    "MosaicRefAcqTimes": ("0019", "1029"),
}
