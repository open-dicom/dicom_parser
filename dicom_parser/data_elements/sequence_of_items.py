import pandas as pd

from dicom_parser.data_element import DataElement
from pydicom.dataset import Dataset as PydicomDataset
from dicom_parser.utils.format_header_df import format_header_df
from dicom_parser.utils.value_representation import ValueRepresentation


class SequenceOfItems(DataElement):
    VALUE_REPRESENTATION = ValueRepresentation.SQ

    def parse_value(self, value: PydicomDataset) -> list:
        raise NotImplementedError(
            "SequenceOfItems data element values should be assigned externally."
        )

    def __str__(self) -> str:
        df = self.to_dataframe()
        info = f"Tag:\t\t{self.tag}\nKeyword:\t{self.keyword}\n\n"
        return info + format_header_df(df, max_colwidth=25) + "\n\n"

    def __repr__(self) -> str:
        return self.__str__()

    def to_dataframe(self) -> pd.DataFrame:
        df = pd.concat(
            [subheader.to_dataframe() for subheader in self.value],
            keys=range(len(self.value)),
            names=("Index", "Tag"),
        )
        df.name = f"{self.tag}\t{self.keyword}"
        return df
