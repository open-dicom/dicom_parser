Quickstart
==========


Coversion to Python's native types
----------------------------------

The most basic usage case is reading a single DICOM image (*.dcm* file).

.. code:: python

    from dicom_parser import Image

    # Create a DICOM Image object

Integer String (IS) to *int*:

.. code:: python

    raw_value = image.header.raw['InstanceNumber'].value
    raw_value
    >> "1"
    type(raw_value)
    >> str

    fixed_value = image.header['InstanceNumber']
    fixed_value
    >> 1
    type(fixed_value)
    >> int

Decimal String (DS) to *float*:

.. code:: python

    # Decimal String (DS) to float
    raw_value = image.header.raw['ImagingFrequency'].value
    raw_value
    >> "123.25993"
    type(raw_value)
    >> str

    fixed_value = image.header['ImagingFrequency']
    fixed_value
    >> 123.25993
    type(fixed_value)
    >> float

Et cetera.

Read DICOM series directory as a :class:`~dicom_parser.series.Series`
---------------------------------------------------------------------

Another useful class this package offers is the
:class:`~dicom_parser.series.Series` class:

.. code:: python

    from dicom_parser import Series

    series = Series('/path/to/dicom/series/')
    series.data.shape
    >> (224, 224, 208)
    series.images[6].header.get('InstanceNumber')
    >> 7    # Images are 1-indexed


Supports for Siemens' CSA headers
---------------------------------
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
