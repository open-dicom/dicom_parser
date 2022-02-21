import os
from datetime import datetime
from pathlib import Path

from dicom_parser.utils.choice_enum import ChoiceEnum

TESTS_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
TEST_FILES_PATH = os.path.join(TESTS_DIRECTORY, "files")
TEST_IMAGE_PATH = os.path.join(TEST_FILES_PATH, "001.dcm")
TEST_MPRAGE_IMAGE_PATH = os.path.join(TEST_FILES_PATH, "mprage", "1.dcm")
TEST_EP2D_IMAGE_PATH = os.path.join(TEST_FILES_PATH, "ep2d_image.dcm")
TEST_RSFMRI_SERIES_PATH = os.path.join(TEST_FILES_PATH, "rsfmri")
TEST_MIME_SERIES_PATH = os.path.join(TEST_FILES_PATH, "rsfmri_mime")
TEST_RSFMRI_IMAGE_PATH = os.path.join(TEST_FILES_PATH, "rsfmri", "001.dcm")
TEST_RSFMRI_IMAGE_VOLUME = os.path.join(
    TEST_FILES_PATH, "rsfmri", "volume.npy"
)
TEST_RSFMRI_SERIES_NIFTI = os.path.join(
    TEST_RSFMRI_SERIES_PATH, "converted.nii.gz"
)
TEST_RSFMRI_SERIES_PIXEL_ARRAY = os.path.join(
    TEST_RSFMRI_SERIES_PATH, "rsfmri.npy"
)
TEST_GE_LOCALIZER_PATH = os.path.join(TEST_FILES_PATH, "GE_localizer.dcm")
TEST_SIEMENS_DWI_PATH = os.path.join(TEST_FILES_PATH, "siemens_dwi", "1.dcm")
TEST_SERIES_PATH = os.path.join(TEST_FILES_PATH, "series")
TEST_UTILS_DIRECTORY = os.path.join(TESTS_DIRECTORY, "utils")
TEST_MULTIFRAME = os.path.join(TEST_FILES_PATH, "4d_multiframe_test.dcm")


TEST_FIELDS = {
    "StudyDate": datetime.strptime("20180501", "%Y%m%d").date(),
}


SERIES_INSTANCE_UID = (
    "1.3.12.2.1107.5.2.43.66024.2018050112250992296484473.0.0.0"
)
SERIES_SPATIAL_RESOLUTION = (0.48828125, 0.48828125, 6.0)
SOP_INSTANCE_UID = "1.3.12.2.1107.5.2.43.66024.2018050112252318571884482"
STUDY_INSTANCE_UID = "1.3.12.2.1107.5.2.43.66024.30000018050107081466900000007"
TEST_IMAGE_RELATIVE_PATH = Path(f"012345678/{SERIES_INSTANCE_UID}/1.dcm")
TEST_DATA_ELEMENT_STRING = """tag                     (0010, 0020)
keyword                    PatientID
value_representation     Long String
value_multiplicity                 1
value                      012345678"""
TEST_DATA_ELEMENT_BYTES_VALUE: str = "HC1-7;NC1"

TEST_ASCCONV_SAMPLE = os.path.join(TEST_FILES_PATH, "ascconv_sample.txt")


class ChoiceEnumDefinition(ChoiceEnum):
    A = "A"
    B = "B"
    C = "C"
