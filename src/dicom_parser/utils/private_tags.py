"""
Definition of the :attr:`PRIVATE_TAGS` dictionary.
"""
from dicom_parser.utils.siemens.private_tags import SIEMENS_PRIVATE_TAGS

#: A dictionary used to associate the keywords of private data elements with
#: their respective tags.
PRIVATE_TAGS = {"SIEMENS": SIEMENS_PRIVATE_TAGS}
