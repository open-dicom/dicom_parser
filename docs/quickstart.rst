Quickstart
==========

The :class:`~dicom_parser.image.Image` Class
--------------------------------------------

The most basic usage case is reading a single DICOM image (*.dcm* file) as
an :class:`~dicom_parser.image.Image` instance.

.. code:: python

    >>> from dicom_parser import Image
    >>> image = Image('/path/to/dicom/file.dcm')


Images have a :attr:`~dicom_parser.image.Image.header` attribute, which stores
the parsed :class:`~dicom_parser.header.Header` instance.

.. code:: python

    >>> image.header
                 Keyword                      VR                VM  Value
    Tag
    (0008, 0005)  SpecificCharacterSet         Code String       1   ISO_IR 100
    (0008, 0008)  ImageType                    Code String       5   ('ORIGINAL', 'PRIMARY', ...
    (0008, 0012)  InstanceCreationDate         Date              1   2018-05-01
    ...

`dicom_parser` provides :obj:`dict`-like access to the parsed values of the
header_\'s data-elements. The raw values as read by pydicom_ remain accessible
through the :attr:`~dicom_parser.header.Header.raw` attribute. For a full
comparison of the expected return types, see :ref:`value-representation`.

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

The :class:`~dicom_parser.series.Series` Class
----------------------------------------------

Another useful class this package offers is the
:class:`~dicom_parser.series.Series` class, which enables reading an entire
series' directory.

.. code:: python

    >>> from dicom_parser import Series
    >>> series = Series('/some/dicom/series/')


Header Information
..................

We can easily query the underlying images' headers using the
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

Image Instances
###############

Another useful feature of the indexing operator is for querying an
:class:`~dicom_parser.image.Image` instance based on its index in the series:

.. code:: python

    >>> series[6]
    dicom_parser.image.Image
    >>> series[6].header['InstanceNumber]
    7   # InstanceNumber is 1-indexed


Pixel Arrays
............

The `data` property returns a stacked volume of the images' pixel arrays:

.. code:: python

    >>> type(series.data)
    numpy.ndarray
    >>> series.data.shape
    (224, 224, 208)

.. _header:
   https://dcm4che.atlassian.net/wiki/spaces/d2/pages/1835038/A+Very+Basic+DICOM+Introduction
.. _pydicom:
   https://pydicom.github.io/