.. _multi-frame:

Multi-frame
===========

Multi-frame DICOM images are supported, and the returned pixel arrays will be
parsed automatically:

.. code-block:: python

    >>> image = Image("/path/to/multi-frame/")
    >>> i.raw.pixel_array.shape
    (112, 512, 512)
    >>> i.data.shape
    (512, 512, 56, 2)

The associated :class:`~dicom_parser.utils.multi_frame.multi_frame.MultiFrame`
instance and underlying attributes are available through the
:attr:`~dicom_parser.image.Image.multi_frame` property.

.. code-block:: python

    >>> type(image.multi_frame)
    dicom_parser.utils.multi_frame.multi_frame.MultiFrame
    >>> i.multi_frame.image_orientation_patient
    array([[ 1.,  0.],
           [ 0.,  0.],
           [ 0., -1.]])
