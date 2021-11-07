"""
Definition of the :class:`PersonName` class, representing a single "PN" data
element.
"""
from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation
from pydicom.valuerep import PersonName as PydicomPersonName


class PersonName(DataElement):
    #: The VR value of data elements represented by this class.
    VALUE_REPRESENTATION = ValueRepresentation.PN

    #: Person name components as defined by the DICOM standard.
    COMPONENTS = (
        "name_prefix",
        "given_name",
        "middle_name",
        "family_name",
        "name_suffix",
    )

    def parse_value(self, value: PydicomPersonName) -> dict:
        """
        Returns a dictionary representation of the "PN" data element's value.

        Parameters
        ----------
        value : PydicomPersonName
            pydicom's "PN" data element representation

        Returns
        -------
        dict
            Parsed person name components
        """

        if isinstance(value, PydicomPersonName):
            return {
                component: getattr(value, component)
                for component in self.COMPONENTS
            }
        return value if value else {}
