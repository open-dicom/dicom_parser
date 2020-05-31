[![PyPI version](https://img.shields.io/pypi/v/dicom_parser.svg)](https://pypi.python.org/pypi/pylabber/)
[![PyPI status](https://img.shields.io/pypi/status/dicom_parser.svg)](https://pypi.python.org/pypi/pylabber/)
[![CircleCI](https://circleci.com/gh/ZviBaratz/dicom_parser.svg?style=shield)](https://app.circleci.com/pipelines/github/ZviBaratz/dicom_parser)
[![codecov.io](https://codecov.io/gh/ZviBaratz/dicom_parser/coverage.svg?branch=master)](https://codecov.io/github/ZviBaratzabbingProject/dicom_parser?branch=master)
[![Documentation Status](https://readthedocs.org/projects/dicom-parser/badge/?version=latest)](http://dicom-parser.readthedocs.io/?badge=latest)

# dicom_parser

_dicom_parser_ is a utility python package meant to facilitate access to
[DICOM](https://www.dicomstandard.org/) header information by extending the functionality of _[pydicom]_.

Essentially, _dicom_parser_ uses [DICOM](https://www.dicomstandard.org/)'s
[data-element](https://northstar-www.dartmouth.edu/doc/idl/html_6.2/DICOM_Attributes.html)
[value-representation (VR)](http://dicom.nema.org/medical/dicom/current/output/chtml/part05/sect_6.2.html),
as well as prior knowledge on vendor-specific private tags or encoding schemes,
in order to transform them to more "pythonic" data structures when possible.

For more information, please see [the documentation].

---

## Installation

To install the latest version of `dicom_parser`, simply run:

```bash
    pip install dicom_parser
```

---

## Quickstart

The most basic usage case is reading a single DICOM image (_.dcm_ file) as
an [Image](https://dicom-parser.readthedocs.io/en/latest/modules/dicom_parser.html#dicom_parser.image.Image)
instance.

```python
    >>> from dicom_parser import Image
    >>> image = Image('/path/to/dicom/file.dcm')
```

### Coversion to Python's native types

_dicom_parser_ provides _dict_-like access to the parsed values of the
[header](https://dcm4che.atlassian.net/wiki/spaces/d2/pages/1835038/A+Very+Basic+DICOM+Introduction)'s
data-elements. The raw values as read by _[pydicom]_ remain accessible through the _raw_ attribute.

#### Examples

Decimal String (DS) to _float_ using the [Header] class's
[get](https://dicom-parser.readthedocs.io/en/latest/modules/dicom_parser.html#dicom_parser.header.Header.get)
method:

```python
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
```

Age String (AS) to _float_:

```python
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
```

Date String (DA) to _[datetime.date]_ using the [Header] class's
indexing operator/subscript notation:

```python
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
```

Code String (CS) to a verbose value or set of values:

```python
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
```

Et cetera.

> The _dict_-like functionality also includes safe getting:
>
> ```python
>     >>> image.header.get('MissingKey')
>     None
>     >>> image.header.get('MissingKey', 'DefaultValue')
>     'DefaultValue'
> ```
>
> As well as raising a KeyError for missing keys with the indexing operator:
>
> ```python
>     >>> image.header['MissingKey']
>     KeyError: "The keyword: 'MissingKey' does not exist in the header!"
> ```

### Read DICOM series directory as a `Series`

Another useful class this package offers is the `Series` class:

```python
    >>> from dicom_parser import Series
    >>> series = Series('/some/dicom/series/')
```

The `Series` instance allows us to easily
query the underlying images' headers using its `get` method:

```python
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
```

Similarly to the `Image` class, we can also use the indexing operator:

```python
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
```

Another useful feature of the indexing operator is for querying an `Image` instance based on its index in the series:

```python
    >>> series[6]
    dicom_parser.image.Image
    >>> series[6].header['InstanceNumber]
    7   # InstanceNumber is 1-indexed
```

The `data` property returns a stacked volume of the images' data:

```python
    >>> type(series.data)
    numpy.ndarray
    >>> series.data.shape
    (224, 224, 208)
```

#### Siemens 4D data

Reading Siemens 4D data
[encoded as mosaics](https://nipy.org/nibabel/dicom/dicom_mosaic.html)
is also supported:

```python
    >>> fmri_series = Series('/path/to/dicom/fmri/')
    >>> fmri_series.data.shape
    (96, 96, 64, 200)
```

[datetime.date]: https://docs.python.org/3/library/datetime.html#available-types
[header]: https://dicom-parser.readthedocs.io/en/latest/modules/dicom_parser.html#dicom_parser.header.Header
[pydicom]: https://pydicom.github.io/
[series]: https://dicom-parser.readthedocs.io/en/latest/modules/dicom_parser.html#dicom_parser.series.Series
[the documentation]: http://dicom-parser.readthedocs.io/?badge=latest
