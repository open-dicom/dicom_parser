Overview
========

`dicom_parser` is a utility python package meant to facilitate access to
`DICOM <https://www.dicomstandard.org/>`_ header information by extending the functionality of
`pydicom <https://github.com/pydicom/pydicom>`_.

Essentially, `dicom_parser` uses `DICOM <https://www.dicomstandard.org/>`_'s
`data-element <https://northstar-www.dartmouth.edu/doc/idl/html_6.2/DICOM_Attributes.html>`_
`value-representation (VR) <http://dicom.nema.org/medical/dicom/current/output/chtml/part05/sect_6.2.html>`_,
as well as prior knowledge on vendor-specific private tags or encoding schemes,
in order to transform them to more "pythonic" data structures when possible.
