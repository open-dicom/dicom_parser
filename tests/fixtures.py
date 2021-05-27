import os
from datetime import datetime
from pathlib import Path

from dicom_parser.utils.choice_enum import ChoiceEnum

TESTS_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
TEST_FILES_PATH = os.path.join(TESTS_DIRECTORY, "files")
TEST_IMAGE_PATH = os.path.join(TEST_FILES_PATH, "001.dcm")
TEST_EP2D_IMAGE_PATH = os.path.join(TEST_FILES_PATH, "ep2d_image.dcm")
TEST_RSFMRI_SERIES_PATH = os.path.join(TEST_FILES_PATH, "rsfmri")
TEST_RSFMRI_IMAGE_PATH = os.path.join(TEST_FILES_PATH, "rsfmri", "001.dcm")
TEST_RSFMRI_IMAGE_VOLUME = os.path.join(
    TEST_FILES_PATH, "rsfmri", "volume.npy"
)
TEST_RSFMRI_SERIES_NIFTI = os.path.join(
    TEST_RSFMRI_SERIES_PATH, "converted.nii.gz"
)
TEST_GE_LOCALIZER_PATH = os.path.join(TEST_FILES_PATH, "GE_localizer.dcm")
TEST_SIEMENS_DWI_PATH = os.path.join(TEST_FILES_PATH, "siemens_dwi", "1.dcm")
TEST_SERIES_PATH = os.path.join(TEST_FILES_PATH, "series")
TEST_UTILS_DIRECTORY = os.path.join(TESTS_DIRECTORY, "utils")
TEST_OW_ELEMENT = (0x00720069, "OW", b"Test")
TEST_OW_EXPECTED = [v for v in TEST_OW_ELEMENT[-1]]


TEST_FIELDS = {
    "InstanceNumber": 1,
    "StudyID": "1.3.12.2.1107.5.2.43.66024.30000018050107081466900000007",
    "StudyDescription": "YA_lab^Assi",
    "StudyDate": datetime.strptime("20180501", "%Y%m%d").date(),
    "StudyTime": datetime.strptime("12:21:56.958000", "%H:%M:%S.%f").time(),
    "PixelSpacing": (0.48828125, 0.48828125),
    "PatientAge": 27.0,
    "SequenceVariant": ("Spoiled", "Oversampling Phase"),
    "SelectorOWValue": TEST_OW_EXPECTED,
}

PARSED_B_MATRIX = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
PARSED_DIFFUSTION_GRADIENT_DIRECTION = [0.57735026, 0.57735038, 0.57735032]

SERIES_INSTANCE_UID = (
    "1.3.12.2.1107.5.2.43.66024.2018050112250992296484473.0.0.0"
)
SERIES_SPATIAL_RESOLUTION = (0.48828125, 0.48828125, 6.0)
SOP_INSTANCE_UID = "1.3.12.2.1107.5.2.43.66024.2018050112252318571884482"
STUDY_INSTANCE_UID = "1.3.12.2.1107.5.2.43.66024.30000018050107081466900000007"
TEST_IMAGE_RELATIVE_PATH = Path(f"012345678/{SERIES_INSTANCE_UID}/1.dcm")


class ChoiceEnumDefinition(ChoiceEnum):
    A = "A"
    B = "B"
    C = "C"
