from dicom_parser.utils.sequence_detector.sequences.mr.anat import (
    MR_ANATOMICAL_SEQUENCES,
)
from dicom_parser.utils.sequence_detector.sequences.mr.dwi import (
    MR_DIFFUSION_SEQUENCES,
)
from dicom_parser.utils.sequence_detector.sequences.mr.func import (
    MR_FUNCTIONAL_SEQUENCES,
)
from dicom_parser.utils.sequence_detector.sequences.mr.physio import (
    MR_PHYSIOLOGICAL_RULES,
)

MR_SEQUENCE_RULES = {
    **MR_ANATOMICAL_SEQUENCES,
    **MR_DIFFUSION_SEQUENCES,
    **MR_FUNCTIONAL_SEQUENCES,
    **MR_PHYSIOLOGICAL_RULES,
}
