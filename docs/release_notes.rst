Release Notes
=============

0.1.3
-----

    * Changed Code String (CS) parsing to return verbose value or set of values using the :mod:`~dicom_parser.utils.code_strings` module. This feature can be disabled by setting the :class:`~dicom_parser.parser.Parser`'s `verbose_code_strings` attribute to `False`.

    * Added warnings for invalid pixel arrays and invalid Code String (CS) values.

    * Updated the :mod:`~dicom_parser.utils.sequence_detector.sequences` class to work with verbose Code String (CS) data element values and renamed known MR sequences.

    * Refactored the :class:`~dicom_parser.parser.Parser` class to a bit to improve readability.

    * Fixed CSA header bug for headers with a duplicate "### ASCCONV END ###" pattern.


0.1.2
-----

    * Improved private tags definition so that the :class:`~dicom_parser.header.Header` model's :meth:`~dicom_parser.header.Header.get` method will work using the private tag's keyword.

    * Added support for calling len() over a :class:`~dicom_parser.series.Series` instance to return the number of images in it.

    * Added support for querying header information from a :class:`~dicom_parser.series.Series` instance using the :meth:`~dicom_parser.series.Series.get` method or the indexing operator ([]) using a `str` or a `tuple`.

    * Added support for indexing the :class:`~dicom_parser.image.Image` instances  from a :class:`~dicom_parser.series.Series` using an `int` or `slice`.


0.1.1
-----

    * Improved support for accessing `CSA headers`_.

    * Added auto-decoding for `Siemens mosaic`_ encoded data (applies to data extraction in both :class:`~dicom_parser.image.Image` and :class:`~dicom_parser.series.Series` instances).

        * The decoding method also changes the orientation of the stacked arrays to match the product of conversion to `NIfTI`_ using `dcm2niix`_.


0.1.0
-----

First release!

    * Type correction based on `value-representation (VR)`_.

    * Simple :class:`~dicom_parser.series.Series` class for reading DICOM series directories.

    * Basic support for reading `CSA headers`_ using the :class:`~dicom_parser.utils.siemens.csa.header.CsaHeader` class.


.. _CSA Headers: https://nipy.org/nibabel/dicom/siemens_csa.html
.. _dcm2niix: https://github.com/rordenlab/dcm2niix
.. _NIfTI: https://nifti.nimh.nih.gov/
.. _Siemens mosaic: https://nipy.org/nibabel/dicom/dicom_mosaic.html
.. _value-representation (VR): http://dicom.nema.org/medical/dicom/current/output/chtml/part05/sect_6.2.html