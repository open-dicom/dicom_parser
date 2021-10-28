"""
Fixtures for data element tests.
"""
import os
from datetime import date, time

import numpy as np

# pickle5 is required for to parse the pickled fixtures in Python before 3.8.
try:
    import pickle5 as pickle
except ModuleNotFoundError:
    import pickle

from dicom_parser.utils.value_representation import ValueRepresentation
from tests.fixtures import TEST_FILES_PATH

#: Expected parsed values to test age string (AS) data elements with.
AGE_STRINGS = {
    "PatientAge": 27.0,
}

#: Expected parsed values to test code string (CS) data elements with.
CODE_STRINGS = {
    "Modality": "Magnetic Resonance",
    "PatientSex": "Male",
    "ScanOptions": ("PFP", "SFS"),
    "SequenceVariant": ("Segmented k-Space", "Spoiled"),
}

#: Expected parsed values to test date (DA) data elements with.
DATES = {
    "InstanceCreationDate": date(2018, 5, 1),
    "PatientBirthDate": date(1990, 12, 14),
}

#: Expected parsed values to test decimal strings (DS) data elements with.
DECIMAL_STRINGS = {
    "PatientSize": 1.86,
    "PatientWeight": 67,
    "SliceThickness": 6,
    "ImagingFrequency": 123.25993,
    "SpacingBetweenSlices": 19.5,
    "PixelSpacing": (0.48828125, 0.48828125),
    "ImageOrientationPatient": (0.0, 1.0, 0.0, 0.0, 0.0, -1.0),
}

#: Expected parsed values to test integer string (IS) data elements with.
INTEGER_STRINGS = {
    "EchoNumbers": 1,
    "NumberOfPhaseEncodingSteps": 233,
    "EchoTrainLength": 1,
    "AcquisitionNumber": 1,
}

#: Expected parsed values to test long string (LO) data elements with.
LONG_STRINGS = {
    "PatientID": "012345678",
    "Manufacturer": "SIEMENS",
    "InstitutionName": "Tel-Aviv University",
}

#: Expected parsed values to test person names (PN) data elements with.
PERSON_NAMES = {
    "ReferringPhysicianName": {},
    "OperatorsName": {
        "name_prefix": "",
        "given_name": "",
        "middle_name": "",
        "family_name": "Irina",
        "name_suffix": "",
    },
    "PatientName": {
        "name_prefix": "",
        "given_name": "Zvi",
        "middle_name": "",
        "family_name": "Baratz",
        "name_suffix": "",
    },
}

#: Expected parsed values to test short text (ST) data elements with.
SHORT_TEXTS = {
    "InstitutionAddress": "Street StreetNo,.,District,IL,ZIP",
    "CommentsOnThePerformedProcedureStep": "",
}

#: Expected parsed values to test short string (SH) data elements with.
SHORT_STRINGS = {
    "StationName": "AWP66024",
    "SequenceName": "*fl2d1",
    "TransmitCoilName": "Body",
    "PerformedProcedureStepID": "MR20180501122157",
}

#: Expected parsed values to test time (TM) data elements with.
TIMES = {
    "InstanceCreationTime": time(12, 25, 23, 268000),
    "StudyTime": time(12, 21, 56, 958000),
    "SeriesTime": time(12, 25, 23, 265000),
}

#: Expected parsed values to test unique identifier (UI) data elements with.
UNIQUE_IDENTIFIERS = {
    "SOPClassUID": "1.2.840.10008.5.1.4.1.1.4",
    "SOPInstanceUID": "1.3.12.2.1107.5.2.43.66024.2018050112252318571884482",
}

#: Expected parsed values to test unsigned short (US) data elements with.
UNSIGNED_SHORTS = {
    "AcquisitionMatrix": (0, 256, 233, 0),
    "SamplesPerPixel": 1,
    "Columns": 512,
    "BitsStored": 12,
    "PixelRepresentation": 0,
    "LargestImagePixelValue": 777,
}

#: Expected parsed values to test byte-encoded private data elements (UN) with
#: no special method dispatch.
PRIVATE_DATA_ELEMENTS = {
    (0x19, 0x100F): "Normal",
    (0x51, 0x1019): "A2",
    (0x29, 0x1018): "MR",
}

#: Path of a pickled parsed CSA header.
TEST_CSA_PATH = os.path.join(TEST_FILES_PATH, "csa.pickle")

with open(TEST_CSA_PATH, "rb") as f:
    #: Parsed CSA header serialized as a Python dictionary.
    CSA_DATA = pickle.load(f)

#: Expected parsed values of various private Siemens elements.
SIEMENS_DWI_ELEMENTS = {
    (0x19, 0x100A): 9,
    (0x19, 0x100B): 77000.0,
    (0x19, 0x100C): 0,
    (0x19, 0x100E): [0.57735026, 0.57735038, 0.57735032],
    (0x19, 0x1027): np.array(
        [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]
    ),
    (0x19, 0x1028): 22.321,
    (0x19, 0x1029): [
        0.0,
        1380.0,
        277.5,
        1655.0,
        552.5,
        1930.0,
        827.5,
        2205.0,
        1102.5,
    ],
    (0x29, 0x1020): CSA_DATA,
}

TEST_OW_ELEMENT = (0x00720069, "OW", b"Test")
TEST_OW_EXPECTED = [v for v in TEST_OW_ELEMENT[-1]]

#: Dictionary of values to compare data element classes' parsed values against.
VR_TO_VALUES = {
    ValueRepresentation.AS: AGE_STRINGS,
    ValueRepresentation.CS: CODE_STRINGS,
    ValueRepresentation.DA: DATES,
    ValueRepresentation.DS: DECIMAL_STRINGS,
    ValueRepresentation.IS: INTEGER_STRINGS,
    ValueRepresentation.LO: LONG_STRINGS,
    ValueRepresentation.PN: PERSON_NAMES,
    ValueRepresentation.SH: SHORT_STRINGS,
    ValueRepresentation.ST: SHORT_TEXTS,
    ValueRepresentation.TM: TIMES,
    ValueRepresentation.UI: UNIQUE_IDENTIFIERS,
    ValueRepresentation.US: UNSIGNED_SHORTS,
}
