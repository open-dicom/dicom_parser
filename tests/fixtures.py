import os

from datetime import datetime

TEST_FILES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "files")
TEST_IMAGE_PATH = os.path.join(TEST_FILES_PATH, "001.dcm")
TEST_DWI_IMAGE_PATH = os.path.join(TEST_FILES_PATH, "dwi_image.dcm")


TEST_STUDY_FIELDS = {
    "uid": "1.3.12.2.1107.5.2.43.66024.30000018050107081466900000007",
    "description": "YA_lab^Assi",
    "date": datetime.strptime("20180501", "%Y%m%d").date(),
    "time": datetime.strptime("12:21:56.958000", "%H:%M:%S.%f").time(),
}
