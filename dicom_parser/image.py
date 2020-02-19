from dicom_parser.header import Header
from dicom_parser.parser import Parser
from dicom_parser.utils.read_file import read_file


class Image:
    def __init__(self, raw, parser=Parser):
        self.raw = read_file(raw, read_data=True)
        self.header = Header(self.raw, parser=parser)
        self.data = self.raw.pixel_array
