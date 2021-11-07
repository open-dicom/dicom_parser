from dicom_parser.utils.sequence_detector.sequences.mr.dwi.diffusion import (
    DWI_RULES,
)
from dicom_parser.utils.sequence_detector.sequences.mr.dwi.fieldmap import (
    DWI_FIELDMAP_RULES,
)

MR_DIFFUSION_SEQUENCES = {
    "dwi": DWI_RULES,
    "dwi_fieldmap": DWI_FIELDMAP_RULES,
}
