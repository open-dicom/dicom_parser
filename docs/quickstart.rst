Quickstart
==========

The most basic usage case is reading a single DICOM image (*.dcm* file) as
an :class:`~dicom_parser.image.Image` instance.

.. code:: python

    from dicom_parser import Image

    # Create a DICOM Image object
    image = Image('/path/to/dicom/file.dcm')


---------------------------------------------------------------


Coversion to Python's native types
----------------------------------

`dicom_parser` provides *dict*-like access to the parsed values of the
`header <https://dcm4che.atlassian.net/wiki/spaces/d2/pages/1835038/A+Very+Basic+DICOM+Introduction>`_'s
data-elements. The raw values as read by `pydicom <https://pydicom.github.io/>`_
remain accessible through the *raw* attribute.

Examples
........

Decimal String (DS) to *float* using the :class:`~dicom_parser.header.Header`
class's :meth:`~dicom_parser.header.Header.get` method:

.. code:: python

    raw_value = image.header.raw['ImagingFrequency'].value
    raw_value
    >> "123.25993"
    type(raw_value)
    >> str

    parsed_value = image.header.get('ImagingFrequency')
    parsed_value
    >> 123.25993
    type(parsed_value)
    >> float

Age String (AS) to *float*:

.. code:: python

    raw_value = image.header.raw['PatientAge'].value
    raw_value
    >> "027Y"
    type(raw_value)
    >> str

    parsed_value = image.header.get('PatientAge')
    parsed_value
    >> 27.0
    type(parsed_value)
    >> float


Date String (DA) to `datetime.date <https://docs.python.org/3/library/datetime.html#available-types>`_
using the :class:`~dicom_parser.header.Header` class's indexing operator/subscript notation:

.. code:: python

    raw_value = image.header.raw['PatientBirthDate'].value
    raw_value
    >> "19901214"
    type(raw_value)
    >> str

    parsed_value = image.header['PatientBirthDate']
    parsed_value
    >> datetime.date(1990, 12, 14)
    type(parsed_value)
    >> datetime.date


Et cetera.

.. note::

    The *dict*-like functionality also includes safe getting:

    .. code:: python

        image.header.get('MissingKey')
        >> None

        image.header.get('MissingKey', 'DefaultValue')
        >> 'DefaultValue'

    As well as raising a KeyError for missing keys with the indexing operator:

    .. code::

        image.header['MissingKey']
        >> ...
        >> KeyError: "The keyword: 'MissingKey' does not exist in the header!"


---------------------------------------------------------------


Read DICOM series directory as a :class:`~dicom_parser.series.Series`
---------------------------------------------------------------------

Another useful class this package offers is the
:class:`~dicom_parser.series.Series` class:

.. code:: python

    from dicom_parser import Series

    anatomical_series = Series('/path/to/dicom/series/')

    # Read stacked pixel arrays as a 3D volume
    type(anatomical_series.data)
    >>> numpy.ndarray
    anatomical_series.data.shape
    >> (224, 224, 208)

    # Access the underlying Image instances
    anatomical_series.images[6].header.get('InstanceNumber')
    >> 7    # instance numbers are 1-indexed

Reading Siemens 4D data
`encoded as mosaics <https://nipy.org/nibabel/dicom/dicom_mosaic.html>`_
is also supported:

.. code:: python

    fmri_series = Series('/path/to/dicom/fmri/')
    fmri_series.data.shape
    >> (96, 96, 64, 200)
