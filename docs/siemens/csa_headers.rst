CSA Headers
===========

Some Siemens MRI scans may include CSA headers that provide valuable information
regarding the acquisition and storage of the data (for more information see
`this <https://nipy.org/nibabel/dicom/siemens_csa.html>`_ excellent
`NiBabel <https://nipy.org/nibabel/index.html>`_ article. These headers are stored as two
`private data elements <http://dicom.nema.org/medical/dicom/current/output/html/part05.html#sect_7.8>`_:

    * (0029, 1010) - CSA Image Header Info
    * (0029, 1020) - CSA Series Header Info

Siemens' CSA headers may easily be parsed using the
:class:`~dicom_parser.utils.siemens.csa.header.CsaHeader` class.

First, let's have a look at the raw value returned by
`pydicom <https://github.com/pydicom/pydicom>`_:

.. code:: python

    from dicom_parser import Image
    from dicom_parser.utils.siemens.csa.header import CsaHeader
    from dicom_parser.utils.siemens.private_tags import SIEMENS_PRIVATE_TAGS

    image = Image('/path/to/siemens/csa.dcm')

    series_header_info_tag = SIEMENS_PRIVATE_TAGS['CSASeriesHeaderInfo'] # == ('0029', '1020')
    raw_csa = image.get(series_header_info_tag)

    # The raw data is returned as bytes
    type(raw_csa)
    >> bytes
    raw_csa[:35]
    >> b"SV10\x04\x03\x02\x01O\x00\x00\x00M\x00\x00\x00UsedPatientWeight\x00\x00\x00\xdc\xf7"


Now, we will create an instance of the
:class:`~dicom_parser.utils.siemens.csa.header.CsaHeader` class and use it to parse the
raw header:

.. code:: python

    # Create an instance of the CsaHeader class
    csa_header = CsaHeader(raw_csa)

    # The CsaHeader class exposes the `parse()` method
    parsed_csa = csa_header.parse()

    type(parsed_csa)
    >> dict

    # Integers are returned as int
    # (we can also use the `parsed` property)
    csa_header.parsed['SliceArray']['Size']
    >> 60

    # Floats are returned as float
    instance_number = image.header.get('InstanceNumber')
    parsed_csa["SliceArray"]["Slice"][instance_number]["Position"]["Tra"]
    >> -58.1979682425

Another option is to simply use the
:class:`~dicom_parser.header.Header` instance's
:meth:`~dicom_parser.header.Header.get_csa` method:

.. code:: python

    csa = image.header.get_csa('CSASeriesHeaderInfo')

    csa.parsed['SliceAcceleration']['MultiBandFactor']
    >> 3
