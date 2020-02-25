Release Notes
=============

0.1.1
-----

    * Improved support for accessing `CSA headers <https://nipy.org/nibabel/dicom/siemens_csa.html>`_.

    * Added auto-decoding for `Siemens mosaic encoded data <https://nipy.org/nibabel/dicom/dicom_mosaic.html>`_ (applies to data extraction in both :class:`~dicom_parser.image.Image` and :class:`~dicom_parser.series.Series` instances).

        * The decoding method also changes the orientation of the stacked arrays to match the product of conversion to `NIfTI <https://nifti.nimh.nih.gov/>`_ using `dcm2niix <https://github.com/rordenlab/dcm2niix>`_.


0.1.0
-----

First release!

    * Type correction based on `value-representation (VR) <http://dicom.nema.org/medical/dicom/current/output/chtml/part05/sect_6.2.html>`_.

    * Simple :class:`~dicom_parser.series.Series` class for reading DICOM series directories.

    * Basic support for reading `CSA headers <https://nipy.org/nibabel/dicom/siemens_csa.html>`_ using the :class:`~dicom_parser.utils.siemens.csa.header.CsaHeader` class.
