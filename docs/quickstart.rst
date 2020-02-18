Quickstart
==========

Header Instantiation
--------------------

To read a DICOM image (`.dcm` file), simply instantiate the
:class:`~dicom_parser.header.Header` class with either a
:class:`~pydicom.FileDataset` instance, a string representing the path of
the `.dcm` file, or a :class:`~pathlib.Path` instance.

String or Path Instantiation Example
....................................

.. code:: python

    from dicom_parser import Header
    from pathlib import Path

    path = "/path/to/some/dicom/image.dcm"
    # or
    path = Path("/path/to/some/dicom/image.dcm")

    header = Header(path)
    
    type(header)
    >> dicom_parser.header.Header

FileDataset Instantiation Example
.................................

.. code:: python

    import pydicom
    from dicom_parser import Header

    path = "/path/to/some/dicom/image.dcm"
    dataset = pydicom.read_file(path)
    header = Header(dataset)
    
    type(header)
    >> dicom_parser.header.Header    


Reading Parsed Values
---------------------

Now, the created :class:`~dicom_parser.header.Header` instance exposes
a :meth:`~dicom_parser.header.Header.get` method that may be used
to retrieve parsed DICOM header values, as well as simply using the
`indexing operator ([]) <https://docs.python.org/3.4/library/operator.html#operator.__getitem__>`_::

    patient_age = header.get('PatientAge')
    # or
    patient_age = header['PatientAge']

    print(patient_age)
    >> 27.0
    type(patient_age)
    >> float

The parsed result may easily be compared with the raw value, as returned
by `pydicom <https://github.com/pydicom/pydicom>`_::

    raw_patient_age = header.get('PatientAge', parsed=False)
    # or
    raw_patient_age = header.get_raw_value('PatientAge')

    print(raw_patient_age)
    >> 027Y
    type(raw_patient_age)
    >> str

.. note::

    Values may also be accessed using a tuple of strings containing the DICOM's
    `data element <https://northstar-www.dartmouth.edu/doc/idl/html_6.2/DICOM_Attributes.html>`_
    tag. In example, to retrieve the
    "`PatientID <https://dicom.innolitics.com/ciods/mr-image/patient/00100020>`_"
    element's value, we may also use::

        header["0010", "0020"]
        >> '012345678'

        # Same as:
        header.get("PatientID")
        >> '012345678'

.. warning::

    Missing keys or tags will return None without raising an error.
