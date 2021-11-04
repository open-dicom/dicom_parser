RAW_ELEMENTS = [
    "GRADSPEC.asGPAData[0].sEddyCompensationY.aflTimeConstant[1]\t = \t0.917683601379",
    "TXSPEC.asNucleusInfo[0].CompProtectionValues.MaxOfflineTxAmpl\t = \t534.113952637",
    "SliceArray.asSlice[2].sNormal.dSag\t = \t-0.01623302609",
    "PtabAbsStartPosZValid\t = \t0x1",
]
LISTED_KEYS = (
    ["GRADSPEC", "GPAData[0]", "EddyCompensationY", "TimeConstant[1]"],
    ["TXSPEC", "NucleusInfo[0]", "CompProtectionValues", "MaxOfflineTxAmpl"],
    ["SliceArray", "Slice[2]", "Normal", "Sag"],
    ["PtabAbsStartPosZValid"],
)
VALUES = ["0.917683601379", "534.113952637", "-0.01623302609", "0x1"]

ARRAY_PATTERNS = "Slice[2]", "NucleusInfo[0]", "TimeConstant[11]"
NON_ARRAY_PATTERNS = "GRADSPEC", "EddyCompensationY", "CompProtectionValues"

ELEMENT_LIST = {"ListKey": [{"FirstElement": "value"}, {"SecondElement": "value"}]}
