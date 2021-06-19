"""
Definition of the :class:`SequenceOfItems` class, representing a single "SQ"
data element.
"""
import pandas as pd
from dicom_parser.data_element import DataElement
from dicom_parser.data_elements.messages import INVALID_SEQUENCE_PARSING
from dicom_parser.utils.format_header_df import format_header_df
from dicom_parser.utils.value_representation import ValueRepresentation
from pydicom.dataset import Dataset as PydicomDataset


class SequenceOfItems(DataElement):
    #: The VR value of data elements represented by this class.
    VALUE_REPRESENTATION = ValueRepresentation.SQ

    def parse_value(self, value: PydicomDataset) -> None:
        """
        Raises *NotImplementedError* as "SQ" data elements in fact represent
        a nested header (see :func:`to_dataframe`).

        Parameters
        ----------
        value : PydicomDataset
            Raw pydicom dataset

        Raises
        ------
        NotImplementedError
            Invalid method
        """
        raise NotImplementedError(INVALID_SEQUENCE_PARSING)

    def __str__(self) -> str:
        """
        Returns the string representing of this instance.
        In this case it is a formatted dataframe containing the nested header's
        information.

        Returns
        -------
        str
            This instance's string representation
        """
        df = self.to_dataframe()
        info = f"Tag:\t\t{self.tag}\nKeyword:\t{self.keyword}\n\n"
        return info + format_header_df(df, max_colwidth=25) + "\n\n"

    def to_dataframe(self) -> pd.DataFrame:
        """
        Converts this "SQ" data element instance's information to a dataframe.

        Returns
        -------
        pd.DataFrame
            This "SQ" data element's information
        """
        df = pd.concat(
            [subheader.to_dataframe() for subheader in self.value],
            keys=range(len(self.value)),
            names=("Index", "Tag"),
        )
        df.name = f"{self.tag}\t{self.keyword}"
        return df
