from dicom_parser.utils.sequence_detector.sequences.mr.func.bold import (
    BOLD_RULES,
)
from dicom_parser.utils.sequence_detector.sequences.mr.func.fieldmap import (
    FUNCTIONAL_FIELDMAP_RULES,
)
from dicom_parser.utils.sequence_detector.sequences.mr.func.sbref import (
    FUNCTIONAL_SBREF_RULES,
)

MR_FUNCTIONAL_SEQUENCES = {
    "bold": BOLD_RULES,
    "func_fieldmap": FUNCTIONAL_FIELDMAP_RULES,
    "func_sbref": FUNCTIONAL_SBREF_RULES,
}
