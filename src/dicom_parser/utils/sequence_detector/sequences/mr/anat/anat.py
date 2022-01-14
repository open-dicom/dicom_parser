from dicom_parser.utils.sequence_detector.sequences.mr.anat.flair import (
    FLAIR_RULES,
)
from dicom_parser.utils.sequence_detector.sequences.mr.anat.fspgr import (
    FSPGR_RULES,
)
from dicom_parser.utils.sequence_detector.sequences.mr.anat.ir_epi import (
    IR_EPI_RULES,
)
from dicom_parser.utils.sequence_detector.sequences.mr.anat.localizer import (
    LOCALIZER_RULES,
)
from dicom_parser.utils.sequence_detector.sequences.mr.anat.mprage import (
    MPRAGE_RULES,
)
from dicom_parser.utils.sequence_detector.sequences.mr.anat.spgr import (
    SPGR_RULES,
)
from dicom_parser.utils.sequence_detector.sequences.mr.anat.t2w import (
    T2W_RULES,
)
from dicom_parser.utils.sequence_detector.sequences.mr.anat.tirm import (
    TIRM_RULES,
)

MR_ANATOMICAL_SEQUENCES = {
    "flair": FLAIR_RULES,
    "ir_epi": IR_EPI_RULES,
    "localizer": LOCALIZER_RULES,
    "mprage": MPRAGE_RULES,
    "spgr": SPGR_RULES,
    "fspgr": FSPGR_RULES,
    "t2w": T2W_RULES,
    "tirm": TIRM_RULES,
}
