import numpy as np


class Data:
    def __init__(self, raw: np.ndarray):
        self.raw = raw

    def fix_mosaic(self) -> np.ndarray:
        """
        Fixes the dimensions of a Siemens EPI pixel data array.
        For more information see pages 10-11
        `here <https://discovery.ucl.ac.uk/id/eprint/1495621/1/Li%20et%20al%20The%20first%20step%20for%20neuroimaging%20data%20analysis%20-%20DICOM%20to%20NIfTI%20conversion.pdf>`_.

        Parameters
        ----------
        data : np.ndarray
            2D pixel data arranged as a mosaic.

        Returns
        -------
        np.ndarray
            3D pixel data arranged as a complete volume.
        """

        return
