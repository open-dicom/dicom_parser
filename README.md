[![Documentation Status](https://readthedocs.org/projects/dicom-parser/badge/?version=latest)](http://dicom-parser.readthedocs.io/?badge=latest)
[![PyPI version](https://img.shields.io/pypi/v/dicom_parser.svg)](https://pypi.python.org/pypi/pylabber/)
[![PyPI status](https://img.shields.io/pypi/status/dicom_parser.svg)](https://pypi.python.org/pypi/pylabber/)
![Coverage](coverage.svg)

# dicom_parser

*dicom_parser* is a utility python package meant to facilitate access to
[DICOM](https://www.dicomstandard.org/) header information by extending the functionality of
[pydicom](https://github.com/pydicom/pydicom).

Essentially, *dicom_parser* uses [DICOM](https://www.dicomstandard.org/)'s
[data-element](https://northstar-www.dartmouth.edu/doc/idl/html_6.2/DICOM_Attributes.html)
[value-representation (VR)](http://dicom.nema.org/medical/dicom/current/output/chtml/part05/sect_6.2.html),
as well as prior knowledge on vendor-specific private tags or encoding schemes,
in order to transform them to more "pythonic" data structures when possible.

For more information, please see
[the documentation](https://readthedocs.org/projects/dicom-parser/badge/?version=latest).