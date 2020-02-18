.. _quickstart: quickstart.html

Overview
========

`dicom_parser` is a utility python package meant to facilitate access to
`DICOM <https://www.dicomstandard.org/>`_ header information by extending the functionality of
`pydicom <https://github.com/pydicom/pydicom>`_.

Essentially, this means that it uses the :class:`~dicom_parser.parser.Parser`
class in order to transform raw DICOM header values to pythonic types according
to their `value-represenation (VR) <http://northstar-www.dartmouth.edu/doc/idl/html_6.2/Value_Representations.html>`_.
These parsed values are easily accessible using the
:class:`~dicom_parser.header.Header` class (see the quickstart_ guide).
