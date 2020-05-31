from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation
from pydicom.valuerep import PersonName


class PersonName(DataElement):
    VALUE_REPRESENTATION = ValueRepresentation.PN
    COMPONENTS = (
        "name_prefix",
        "given_name",
        "middle_name",
        "family_name",
        "name_suffix",
    )

    def parse_value(self, value: PersonName) -> dict:
        if isinstance(value, PersonName):
            return {
                component: getattr(value, component) for component in self.COMPONENTS
            }
        return value
