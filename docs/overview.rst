Overview
========

`dicom_parser` is a utility python package meant to facilitate access to
`DICOM <https://www.dicomstandard.org/>`_ header information by extending the
functionality of `pydicom <https://github.com/pydicom/pydicom>`_.

Essentially, `dicom_parser` uses `DICOM <https://www.dicomstandard.org/>`_'s
`data-element
<https://northstar-www.dartmouth.edu/doc/idl/html_6.2/DICOM_Attributes.html>`_
value representation (VR) and prior knowledge on vendor-specific private tags
or encoding schemes, to **transform raw dicom data to more "pythonic" data
structures** (for a complete comparison, see :ref:`value-representation`).