from dicom_parser.data_elements.age_string import AgeString
from dicom_parser.data_elements.application_entity import ApplicationEntity
from dicom_parser.data_elements.attribute_tag import AttributeTag
from dicom_parser.data_elements.code_string import CodeString
from dicom_parser.data_elements.date import Date
from dicom_parser.data_elements.date_time import DateTime
from dicom_parser.data_elements.decimal_string import DecimalString
from dicom_parser.data_elements.floating_point_double import FloatingPointDouble
from dicom_parser.data_elements.floating_point_single import FloatingPointSingle
from dicom_parser.data_elements.integer_string import IntegerString
from dicom_parser.data_elements.long_string import LongString
from dicom_parser.data_elements.long_text import LongText
from dicom_parser.data_element import DataElement
from dicom_parser.data_elements.other_64bit_very_long import Other64bitVeryLong
from dicom_parser.data_elements.other_byte import OtherByte
from dicom_parser.data_elements.other_double import OtherDouble
from dicom_parser.data_elements.other_float import OtherFloat
from dicom_parser.data_elements.other_long import OtherLong
from dicom_parser.data_elements.other_word import OtherWord
from dicom_parser.data_elements.person_name import PersonName
from dicom_parser.data_elements.private_data_element import PrivateDataElement
from dicom_parser.data_elements.sequence_of_items import SequenceOfItems
from dicom_parser.data_elements.short_string import ShortString
from dicom_parser.data_elements.short_text import ShortText
from dicom_parser.data_elements.signed_64bit_very_long import Signed64bitVeryLong
from dicom_parser.data_elements.signed_long import SignedLong
from dicom_parser.data_elements.signed_short import SignedShort
from dicom_parser.data_elements.time import Time
from dicom_parser.data_elements.unique_identifier import UniqueIdentifer
from dicom_parser.data_elements.unlimited_characters import UnlimitedCharacters
from dicom_parser.data_elements.unlimited_text import UnlimitedText
from dicom_parser.data_elements.unsigned_64bit_very_long import Unsigned64bitVeryLong
from dicom_parser.data_elements.unsigned_long import UnsignedLong
from dicom_parser.data_elements.unsigned_short import UnsignedShort
from dicom_parser.data_elements.url import Url
from dicom_parser.utils.value_representation import (
    ValueRepresentation,
    get_value_representation,
)


VR_TO_DATA_ELEMENT = {
    ValueRepresentation.AS: AgeString,
    ValueRepresentation.AE: ApplicationEntity,
    ValueRepresentation.AT: AttributeTag,
    ValueRepresentation.CS: CodeString,
    ValueRepresentation.DA: Date,
    ValueRepresentation.DT: DateTime,
    ValueRepresentation.DS: DecimalString,
    ValueRepresentation.FD: FloatingPointDouble,
    ValueRepresentation.FL: FloatingPointSingle,
    ValueRepresentation.IS: IntegerString,
    ValueRepresentation.LO: LongString,
    ValueRepresentation.LT: LongText,
    ValueRepresentation.OV: Other64bitVeryLong,
    ValueRepresentation.OB: OtherByte,
    ValueRepresentation.OD: OtherDouble,
    ValueRepresentation.OF: OtherFloat,
    ValueRepresentation.OL: OtherLong,
    ValueRepresentation.OW: OtherWord,
    ValueRepresentation.PN: PersonName,
    ValueRepresentation.SQ: SequenceOfItems,
    ValueRepresentation.SH: ShortString,
    ValueRepresentation.ST: ShortText,
    ValueRepresentation.SV: Signed64bitVeryLong,
    ValueRepresentation.SL: SignedLong,
    ValueRepresentation.SS: SignedShort,
    ValueRepresentation.TM: Time,
    ValueRepresentation.UI: UniqueIdentifer,
    ValueRepresentation.UN: PrivateDataElement,
    ValueRepresentation.UC: UnlimitedCharacters,
    ValueRepresentation.UT: UnlimitedText,
    ValueRepresentation.UV: Unsigned64bitVeryLong,
    ValueRepresentation.UL: UnsignedLong,
    ValueRepresentation.US: UnsignedShort,
    ValueRepresentation.UR: Url,
}


def get_data_element_class(key: str) -> DataElement:
    vr = get_value_representation(key)
    return VR_TO_DATA_ELEMENT[vr]
