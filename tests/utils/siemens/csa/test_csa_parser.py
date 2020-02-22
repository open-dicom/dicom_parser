from dicom_parser.utils.siemens.csa.data_element import CsaDataElement
from dicom_parser.utils.siemens.csa.parser import CsaParser
from tests.utils.siemens.csa.fixtures import ELEMENT_LIST, LISTED_KEYS, RAW_ELEMENTS
from unittest import TestCase


class CsaParserTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.csa_parser = CsaParser()

    def test_parsed_attribute_set_to_dict_on_init(self):
        fresh_parser = CsaParser()
        self.assertDictEqual(fresh_parser.parsed, {})

    def test_update_existing_element_list_with_existing_index(self):
        destination = ELEMENT_LIST.copy()
        part_name = "ListKey"
        index = 1
        expected = destination["ListKey"][index]
        result = self.csa_parser.update_existing_element_list(
            part_name, index, destination
        )
        self.assertIs(result, expected)

    def test_update_existing_element_list_with_missing_index(self):
        destination = ELEMENT_LIST.copy()
        part_name = "ListKey"
        index = 2
        result = self.csa_parser.update_existing_element_list(
            part_name, index, destination
        )
        expected = destination["ListKey"][index]
        self.assertIs(result, expected)

    def test_create_new_element_list(self):
        destination = {}
        part_name = "NewArray"
        result = self.csa_parser.create_new_element_list(part_name, destination)
        expected = destination[part_name][0]
        self.assertIs(result, expected)
        self.assertIsInstance(result, dict)

    def test_scaffold_list_part_with_existing_list(self):
        destination = {
            "ExistingArrayPattern": [{"ElementA": "value"}, {"ElementB": "value"}]
        }
        part_name = "ExistingArrayPattern"
        index = 2
        result = self.csa_parser.scaffold_list_part(part_name, index, destination)
        self.assertIs(result, destination[part_name][index])
        self.assertIsInstance(result, dict)

    def test_scaffold_list_part_with_missing_list(self):
        destination = {
            "ExistingArrayPattern": [{"ElementA": "value"}, {"ElementB": "value"}]
        }
        part_name = "MissingArrayPattern"
        index = 0
        result = self.csa_parser.scaffold_list_part(part_name, index, destination)
        self.assertIs(result, destination[part_name][index])
        self.assertIsInstance(result, dict)

    def test_scaffold_dict_part_with_missing_dict(self):
        destination = {}
        part_name = "MissingPart"
        result = self.csa_parser.scaffold_dict_part(part_name, destination)
        self.assertIs(result, destination[part_name])
        self.assertDictEqual(result, {})

    def test_scaffold_dict_part_with_existing_dict(self):
        destination = {"ExistingPart": {"ExistingSubpart": "value"}}
        part_name = list(destination.keys())[0]
        result = self.csa_parser.scaffold_dict_part(part_name, destination)
        self.assertIs(result, destination[part_name])
        self.assertDictEqual(result, {"ExistingSubpart": "value"})

    # TODO: Complete tests
