Private Tags
============

.. list-table:: CSA Header Information
   :widths: 20 20 40 20
   :header-rows: 1

   * - Tag
     - Keyword
     - Description
     - Return Type
   * - (0029, 1008)
     - CSAImageHeaderType
     - CSA image header type.
     - `str`
   * - (0029, 1009)
     - CSAImageHeaderVersion
     - CSA image header version.
     - `str`
   * - (0029, 1010)
     - CSAImageHeaderInfo
     - CSA image header info.
     - `dict`
   * - (0029, 1018)
     - CSASeriesHeaderType
     - CSA series header type.
     - `str`
   * - (0029, 1019)
     - CSASeriesHeaderVersion
     - CSA series header version.
     - `str`
   * - (0029, 1020)
     - CSASeriesHeaderInfo
     - CSA series header info.
     - `dict`

See also:

    * :ref:`csa-headers` 
    * `NiBabel article`_

.. list-table:: Diffusion-Weighted Imaging
   :widths: 20 20 40 20
   :header-rows: 1

   * - Tag
     - Keyword
     - Description
     - Return Type
   * - (0019, 100a)
     - NumberOfImagesInMosaic
     - Number of images in a mosaic encoded volume.
     - `int`
   * - (0019, 100b)
     - SliceMeasurementDuration
     - Slice measurement duration.
     - `float`
   * - (0019, 100c)
     - B_value
     - b-value.
     - `int`
   * - (0019, 100d)
     - DiffusionDirectionality
     - Diffusion directionality.
     - `str`
   * - (0019, 100e)
     - DiffusionGradientDirection
     - Diffusion gradient direction.
     - `List[float]`
   * - (0019, 100f)
     - GradientMode
     - Gradient mode.
     - `str`
   * - (0019, 1027)
     - B_matrix
     - b matrix.
     - `np.ndarray[(3, 3)]`
   * - (0019, 1028)
     - BandwidthPerPixelPhaseEncode
     - Pixel phase-encoding bandwidth.
     - `float`
   * - (0019, 1029)
     - MosaicRefAcqTimes
     - Relative acquisition times of mosaic slices.
     - `List[float]`

See Also:

    * :ref:`mosaic`
    * `NAMIC Wiki article`_


.. _NAMIC Wiki article:
   https://www.na-mic.org/wiki/NAMIC_Wiki:DTI:DICOM_for_DWI_and_DTI
.. _NiBabel article:
   https://nipy.org/nibabel/dicom/siemens_csa.html