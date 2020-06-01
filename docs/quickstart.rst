Quickstart
==========

The most basic usage case is reading a single DICOM image (*.dcm* file) as
an :class:`~dicom_parser.image.Image` instance.

.. code:: python

    >>> from dicom_parser import Image
    >>> image = Image('/path/to/dicom/file.dcm')

---------------------------------------------------------------

Coversion to Python's native types
----------------------------------

`dicom_parser` provides :obj:`dict`-like access to the parsed values of the
header_\'s data-elements. The raw values as read by pydicom_ remain accessible
through the :attr:`~dicom_parser.header.Header.raw` attribute.

.. _header:
  https://dcm4che.atlassian.net/wiki/spaces/d2/pages/1835038/A+Very+Basic+DICOM+Introduction
.. _pydicom: https://pydicom.github.io/

Examples
........

Decimal String (DS) to :obj:`float` using the :class:`~dicom_parser.header.Header`
class's :meth:`~dicom_parser.header.Header.get` method:

.. code:: python

    >>> raw_value = image.header.raw['ImagingFrequency'].value
    >>> raw_value
    "123.25993"
    >>> type(raw_value)
    str

    >>> parsed_value = image.header.get('ImagingFrequency')
    >>> parsed_value
    123.25993
    >>> type(parsed_value)
    float

Age String (AS) to *float*:

.. code:: python

    >>> raw_value = image.header.raw['PatientAge'].value
    >>> raw_value
    "027Y"
    >>> type(raw_value)
    str

    >>> parsed_value = image.header.get('PatientAge')
    >>> parsed_value
    27.0
    >>> type(parsed_value)
    float


Date String (DA) to `datetime.date`_ using the :class:`~dicom_parser.header.Header`
class's indexing operator/subscript notation:

.. _datetime.date: https://docs.python.org/3/library/datetime.html#available-types

.. code:: python

    >>> raw_value = image.header.raw['PatientBirthDate'].value
    >>> raw_value
    "19901214"
    >>> type(raw_value)
    str

    >>> parsed_value = image.header['PatientBirthDate']
    >>> parsed_value
    datetime.date(1990, 12, 14)
    >>> type(parsed_value)
    datetime.date

Code String (CS) to a verbose value or set of values:

.. code:: python

    >>> raw_value = image.header.raw['SequenceVariant'].value
    >>> raw_value
    ['SP', 'OSP']
    >>> type(raw_value)
    pydicom.multival.MultiValue

    >>> parsed_value = image.header['SequenceVariant']
    >>> parsed_value
    {'Oversampling Phase', 'Spoiled'}
    >>> type(parsed_value)
    set


Et cetera.

.. note::

    The *dict*-like functionality also includes safe getting:

    .. code:: python

        >>> image.header.get('MissingKey')
        None

        >>> image.header.get('MissingKey', 'DefaultValue')
        'DefaultValue'

    As well as raising a KeyError for missing keys with the indexing operator:

    .. code::

        >>> image.header['MissingKey']
        KeyError: "The keyword: 'MissingKey' does not exist in the header!"

---------------------------------------------------------------

Read DICOM series directory as a :class:`~dicom_parser.series.Series`
---------------------------------------------------------------------

Another useful class this package offers is the
:class:`~dicom_parser.series.Series` class:

.. code:: python

    >>> from dicom_parser import Series
    >>> series = Series('/some/dicom/series/')


The :class:`~dicom_parser.series.Series` instance allows us to easily
query the underlying images' headers using its
:meth:`~dicom_parser.series.Series.get` method:

.. code:: python

    # Single value
    >>> series.get('EchoTime')
    3.04

    # Multiple values
    >>> series.get('InstanceNumber')
    [1, 2, 3]

    # No value
    >>> series.get('MissingKey')
    None

    # Default value
    >>> series.get('MissingKey', 'default_value')
    'default_value'

Similarly to the :class:`~dicom_parser.image.Image` class, we can also use
the indexing operator:

.. code:: python

    # Single value
    >>> series['RepetitionTime']
    7.6

    # Multiple values
    >>> series['SOPInstanceUID']
    ["1.123.1241.123124124.12.1",
     "1.123.1241.123124124.12.2",
     "1.123.1241.123124124.12.3"]

    # No value
    >>> series['MissingKey']
    KeyError: "The keyword: 'MissingKey' does not exist in the header!"

Another useful feature of the indexing operator is for querying an
:class:`~dicom_parser.image.Image` instance based on its index in the series:

.. code:: python

    >>> series[6]
    dicom_parser.image.Image
    >>> series[6].header['InstanceNumber]
    7   # InstanceNumber is 1-indexed

The `data` property returns a stacked volume of the images' data:

.. code:: python

    >>> type(series.data)
    numpy.ndarray
    >>> series.data.shape
    (224, 224, 208)



Siemens 4D data
...............

Reading Siemens 4D data
`encoded as mosaics <https://nipy.org/nibabel/dicom/dicom_mosaic.html>`_
is also supported:

.. code:: python

    >>> fmri_series = Series('/path/to/dicom/fmri/')
    >>> fmri_series.data.shape
    (96, 96, 64, 200)
