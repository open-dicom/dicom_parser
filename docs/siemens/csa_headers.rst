CSA Headers
===========

Some Siemens MRI scans may include CSA headers that provide valuable information
regarding the acquisition and storage of the data (for more information see
this_ excellent NiBabel_ article. These headers are stored as two
`private data elements`_:

    * (0029, 1010) - CSA Image Header Info
    * (0029, 1020) - CSA Series Header Info

.. _NiBabel: https://nipy.org/nibabel/index.html
.. _private data elements:
   http://dicom.nema.org/medical/dicom/current/output/html/part05.html#sect_7.8
.. _this: https://nipy.org/nibabel/dicom/siemens_csa.html

By default, the :class:`~dicom_parser.header.Header` instance's
:meth:`~dicom_parser.header.Header.get` method will parsed the CSA header
information as a :obj:`dict`:

.. code:: python

    >>> from dicom_parser import Image
    >>> image = Image('/path/to/siemens/csa.dcm')
    >>> csa = image.header.get('CSASeriesHeaderInfo')
    >>> csa['SliceAcceleration']['MultiBandFactor']
    3

`dicom_parser` uses the :class:`~dicom_parser.utils.siemens.csa.header.CsaHeader`
class in order to created the parsed dictionary.

To learn more about the :class:`~dicom_parser.utils.siemens.csa.header.CsaHeader`
class, let's have a look at the raw CSA header value returned by
pydicom_:

.. _pydicom: https://github.com/pydicom/pydicom

.. code:: python

    >>> from dicom_parser.utils.siemens.csa.header import CsaHeader
    >>> raw_csa = image.header.get('CSASeriesHeaderInfo', parsed=False)
    >>> type(raw_csa)
    bytes
    >>> raw_csa[:35]
    b"SV10\x04\x03\x02\x01O\x00\x00\x00M\x00\x00\x00UsedPatientWeight\x00\x00\x00\xdc\xf7"

Now, we will create an instance of the
:class:`~dicom_parser.utils.siemens.csa.header.CsaHeader` class and use it to parse
the raw header:

.. code:: python

    >>> csa_header = CsaHeader(raw_csa)

    >>> parsed_csa = csa_header.parse()
    >>> type(parsed_csa)
    dict

    # (we can also use the `parsed` property)
    >>> csa_header.parsed['SliceArray']['Size']
    60

    >>> instance_number = image.header.get('InstanceNumber')
    >>> parsed_csa["SliceArray"]["Slice"][instance_number]["Position"]["Tra"]
    -58.1979682425
