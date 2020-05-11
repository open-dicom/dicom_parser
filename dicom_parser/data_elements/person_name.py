from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation
from pydicom.valuerep import PersonName3


class PersonName(DataElement):
    VALUE_REPRESENTATION = ValueRepresentation.PN
    COMPONENTS = (
        "name_prefix",
        "given_name",
        "middle_name",
        "family_name",
        "name_suffix",
    )

    def parse_value(self, value: PersonName3) -> dict:
        if isinstance(value, PersonName3):
            return {
                component: getattr(value, component) for component in self.COMPONENTS
            }
        return value
