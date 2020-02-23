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
:class:`~dicom_parser.utils.siemens.csa.header.CsaHeader` class:

.. code:: python

    from dicom_parser import Image
    from dicom_parser.utils.siemens.csa.header import CsaHeader

    image = Image('/path/to/siemens/csa.dcm')

    raw_csa = image.get(('0029', '1020'))
    type(raw_csa)
    >> bytes
    raw_csa[:35]
    >> b"SV10\x04\x03\x02\x01O\x00\x00\x00M\x00\x00\x00UsedPatientWeight\x00\x00\x00\xdc\xf7"

    csa_header = CsaHeader(raw_csa)
    type(csa_header)
    >> dict
    csa_header['SliceArray']['Size']
    >> "11"

.. note::

    Type conversion for CSA header values is still not implemented.
