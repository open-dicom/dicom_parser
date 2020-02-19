import os

from datetime import datetime
from dicom_parser.utils.choice_enum import ChoiceEnum

TESTS_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
TEST_FILES_PATH = os.path.join(TESTS_DIRECTORY, "files")
TEST_IMAGE_PATH = os.path.join(TEST_FILES_PATH, "001.dcm")
TEST_DWI_IMAGE_PATH = os.path.join(TEST_FILES_PATH, "dwi_image.dcm")
TEST_SERIES_PATH = os.path.join(TEST_FILES_PATH, "series")
TEST_UTILS_DIRECTORY = os.path.join(TESTS_DIRECTORY, "utils")


TEST_STUDY_FIELDS = {
    "uid": "1.3.12.2.1107.5.2.43.66024.30000018050107081466900000007",
    "description": "YA_lab^Assi",
    "date": datetime.strptime("20180501", "%Y%m%d").date(),
    "time": datetime.strptime("12:21:56.958000", "%H:%M:%S.%f").time(),
}


class ChoiceEnumDefinition(ChoiceEnum):
    A = "A"
    B = "B"
    C = "C"
