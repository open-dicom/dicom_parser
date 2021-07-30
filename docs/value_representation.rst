.. _value-representation:

Value Representation
====================

DICOM header fields contain, in the great majority of cases, `Value
Representation (VR)`_ codes that provide information about the type of the data that
is stored or its expected format.

The following table provides an overview of the expected return types by VR:

+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| VR | Name             | *pydicom*                             | *dicom_parser*                      | Comments                          |
+====+==================+=======================================+=====================================+===================================+
| AE | Application      | :class:`str`                          | :class:`str`                        |                                   |
|    | Entity           |                                       |                                     |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| AS | Age String       | :class:`str`                          | :class:`float`                      | Age in years.                     |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| AT | Attribute Tag    | :class:`~pydicom.tag.BaseTag`         | :class:`~pydicom.tag.BaseTag`       |                                   |
|    |                  |                                       |                                     |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| CS | Code String      | :class:`str`                          | :class:`str`                        | Values will, by default, be       |
|    |                  |                                       |                                     | converted to verbose values (if   |
|    |                  |                                       |                                     | available).                       |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| DA | Date             | :class:`str` or                       | :class:`datetime.date`              |                                   |
|    |                  | :class:`~pydicom.valuerep.DA`         |                                     |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| DS | Decimal String   | :class:`~pydicom.valuerep.DSfloat` or | :class:`float`                      |                                   |
|    |                  | :class:`~pydicom.valuerep.DSdecimal`  |                                     |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| DT | Date Time        | :class:`str` or                       | :class:`datetime.datetime`          |                                   |
|    |                  | :class:`~pydicom.valuerep.DT`         |                                     |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| FL | Floating Point   | :class:`float`                        | :class:`float`                      |                                   |
|    | Single           |                                       |                                     |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| FD | Floating Point   | :class:`float`                        | :class:`float`                      |                                   |
|    | Double           |                                       |                                     |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| IS | Integer String   | :class:`~pydicom.valuerep.IS`         | :class:`int`                        |                                   |
|    |                  |                                       |                                     |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| LO | Long String      | :class:`str`                          | :class:`str`                        |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| LT | Long Text        | :class:`str`                          | :class:`str`                        |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| OB | Other Byte       | :class:`bytes`                        | :class:`bytes` or :class:`str`      |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| OD | Other Double     | :class:`bytes`                        | :class:`bytes` or :class:`str`      |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| OF | Other Float      | :class:`bytes`                        | :class:`bytes` or :class:`str`      |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| OL | Other Long       | :class:`bytes`                        | :class:`bytes` or :class:`str`      |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| OV | Other 64-bit     | :class:`bytes`                        | :class:`bytes` or :class:`str`      |                                   |
|    | Very Long        |                                       |                                     |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| OW | Other Word       | :class:`bytes`                        | :class:`bytes` or :class:`str`      |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| PN | Person Name      | :class:`~pydicom.valuerep.PersonName` | :class:`dict`                       |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| SH | Short String     | :class:`str`                          | :class:`str`                        |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| SL | Signed Long      | :class:`int`                          | :class:`int`                        |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| SQ | Sequence of      | :class:`~pydicom.sequence.Sequence`   | :class:`~dicom_parser.header.Header`|                                   |
|    | Items            |                                       |                                     |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| SS | Signed Short     | :class:`int`                          | :class:`int`                        |                                   |
|    |                  |                                       |                                     |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| ST | Short Text       | :class:`str`                          | :class:`str`                        |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| SV | Signed 64-bit    | :class:`int`                          | :class:`int`                        |                                   |
|    | Very Long        |                                       |                                     |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| TM | Time             | :class:`str` or                       | :class:`datetime.time`              |                                   |
|    |                  | :class:`~pydicom.valuerep.TM`         |                                     |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| UC | Unlimited        | :class:`str`                          | :class:`str`                        |                                   |
|    | Characters       |                                       |                                     |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| UI | Unique           | :class:`~pydicom.uid.UID`             | :class:`~pydicom.uid.UID`           |                                   |
|    | Identifier (UID) |                                       |                                     |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| UL | Unsigned Long    | :class:`int`                          | :class:`int`                        |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| UN | Unknown          | :class:`bytes`                        | :class:`bytes` or :class:`str`      |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| UR | URI/URL          | :class:`str`                          | :class:`str`                        |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| US | Unsigned Short   | :class:`int`                          | :class:`int`                        |                                   |
|    |                  |                                       |                                     |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| UT | Unlimited Text   | :class:`str`                          | :class:`str`                        |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+
| UV | Unsigned 64-bit  | :class:`int`                          | :class:`int`                        |                                   |
|    | Very Long        |                                       |                                     |                                   |
+----+------------------+---------------------------------------+-------------------------------------+-----------------------------------+

Examples
--------

Decimal String
##############

Image Frequency String to *float*:

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

Age String
##########

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


Date String
###########

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


Code String
###########

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


.. _pydicom:
   https://pydicom.github.io/
.. _Value Representation  (VR):
   http://dicom.nema.org/medical/dicom/current/output/chtml/part05/sect_6.2.html