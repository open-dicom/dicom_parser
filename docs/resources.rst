Resources
=========

Learning
--------

* `Official DICOM Standard Website`_
* `DICOM Library`_: Free online DICOM file sharing service for educational and
  scientific purposes.
* `dcm4che Wiki`_: Basic introduction to DICOM files and fundamental
  information.
* `DICOM Standard Browser`_: Great online DICOM dictionary and reference.
* `DICOM is Easy`_: Entire blog dedicated to the DICOM file format and software
  programming for medical applications.

Other Tools
-----------

Python
......

* `pydicom`_: The corenerstone for *dicom_parser* and generally an excellent
  resource.
* `dcmstack`_: Summarize datasets and convert to NIfTI.
* `highdicom`_: *"high-level DICOM abstractions for the Python programming
  language to facilitate the creation and handling of DICOM objects for
  image-derived information, including image annotations and image analysis
  results."*
* `dcm`_: *"Python package and CLI application for performing high-level DICOM
  file and network operations."*
* `dicom2nifti`_: General purpose DICOM to NIfTI conversion.

JavaScript
..........
* `cornerstone.js`_: Complete DICOM parsing and visualization suite.
* `dcmjs-org`_: Another large project implementing DICOM in JS.
* `itk.js`_: *itk.js combines Emscripten and ITK to enable high-performance
  spatial analysis in a JavaScript runtime environment.*

C++
...
* `Insight Toolkit (ITK)`_: *"open-source, cross-platform library that provides
  developers with an extensive suite of software tools for image analysis."*
* FreeSurfer's `DICOMRead.cpp`_.
* `MRtrix`_'s `mrconvert`_.
* `dicomtonifti`_: Part of the `vtk-dicom`_ toolkit.
* `dinifti`_: NYU Center for Brain Imaging DICOM to NIfTI converter.

C
...
* `dcm2niix`_: CLI tool (also available through `MRIcroGL`_ and `FSLeyes`_).
  Provides very robust DICOM to NIfTI conversion along with `FSL`_ format
  bvec/bval files and BIDS format JSON files.
* `FreeSurfer`_'s `packages/dicom`_.

MATLAB
......
* `dcm2nii`_: Standard DICOM to NIfTI conversion, includes the FSL format
  bvec/bval files as well as the BIDS format JSON file.
* `SPM12`_, particularly `spm_dicom_convert.m`_.
* `FreeSurfer`_'s `load_dicom_series.m`_ and `load_dicom_fl.m`_.

Rust
....
* `dicom-parser-rs`_

For a more complete discussion of existing DICOM management tools for languages
other than Python, see the `dedicated DICOM discourse thread`_.


.. _cornerstone.js:
   https://github.com/cornerstonejs
.. _dcm:
   https://github.com/moloney/dcm
.. _dcm2niix:
   https://github.com/rordenlab/dcm2niix
.. _dcm2nii:
   https://github.com/xiangruili/dicm2nii
.. _dcm4che Wiki:
   https://dcm4che.atlassian.net/wiki/spaces/d2/pages/1835038/A+Very+Basic+DICOM+Introduction
.. _dcmjs-org:
   https://github.com/dcmjs-org
.. _dcmstack:
   https://github.com/moloney/dcmstack
.. _dicom2nifti:
   https://github.com/icometrix/dicom2nifti
.. _dicomtonifti:
   https://github.com/dgobbi/vtk-dicom/wiki/dicomtonifti
.. _dicom-parser-rs:
   https://github.com/chafey/dicom-parser-rs
.. _dinifti:
   https://as.nyu.edu/cbi/resources/Software/DINIfTI.html
.. _DICOM Library:
   https://www.dicomlibrary.com/
.. _DICOM Standard Browser:
   https://dicom.innolitics.com/
.. _DICOM is Easy:
   http://dicomiseasy.blogspot.com/
.. _DICOMRead.cpp:
   https://github.com/freesurfer/freesurfer/blob/dev/utils/DICOMRead.cpp
.. _dedicated DICOM discourse thread:
   https://nipy.discourse.group/t/dicom-neuroimaging-conversion-packages-based-on-languages-other-than-python/26
.. _FSL:
   https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/
.. _FSLeyes:
   https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FSLeyes
.. _FreeSurfer:
   https://surfer.nmr.mgh.harvard.edu/
.. _highdicom:
   https://github.com/mghcomputationalpathology/highdicom
.. _Insight Toolkit (ITK):
   https://itk.org/
.. _itk.js:
   https://insightsoftwareconsortium.github.io/itk-js/
.. _load_dicom_fl.m:
   https://github.com/freesurfer/freesurfer/blob/dev/matlab/load_dicom_fl.m
.. _load_dicom_series.m:
   https://github.com/freesurfer/freesurfer/blob/dev/matlab/load_dicom_series.m
.. _MRIcroGL:
   https://github.com/rordenlab/MRIcroGL
.. _MRtrix:
   https://mrtrix.readthedocs.io/en/latest/
.. _mrconvert:
   https://mrtrix.readthedocs.io/en/latest/reference/commands/mrconvert.html
.. _Official DICOM Standard Website:
   https://www.dicomstandard.org/
.. _packages/dicom:
   https://github.com/freesurfer/freesurfer/tree/dev/packages/dicom/
.. _pydicom:
   https://pydicom.github.io/
.. _SPM12:
   https://www.fil.ion.ucl.ac.uk/spm/software/spm12/
.. _spm_dicom_convert.m:
   https://github.com/spm/spm12/blob/master/spm_dicom_convert.m
.. _vtk-dicom:
   https://github.com/dgobbi/vtk-dicom