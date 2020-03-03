from dicom_parser.header import Header
from dicom_parser.utils.siemens.csa.header import CsaHeader
from dicom_parser.utils.siemens.csa.parser import CsaParser
from dicom_parser.utils.siemens.private_tags import SIEMENS_PRIVATE_TAGS
from tests.fixtures import TEST_EP2D_IMAGE_PATH
from tests.utils.siemens.csa.fixtures import ELEMENT_LIST
from unittest import TestCase


class CsaParserTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.csa_parser = CsaParser()

        # Read a sample header
        cls.header = Header(TEST_EP2D_IMAGE_PATH)
        csa_series_info_tag = SIEMENS_PRIVATE_TAGS["CSASeriesHeaderInfo"]
        raw_csa_header = cls.header.get(csa_series_info_tag, parsed=False)
        csa_header = CsaHeader(raw_csa_header)
        cls.parsed = csa_header.parse()

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

    def test_parse_return_type(self):
        self.assertIsInstance(self.parsed, dict)
        self.assertEqual(self.parsed["SliceArray"]["Size"], 60)

    def test_parse_int_conversion(self):
        slice_array_size = self.parsed["SliceArray"]["Size"]
        expected = 60
        self.assertEqual(slice_array_size, expected)

    def test_parse_int_conversion_for_floating_point_int(self):
        value = self.parsed["KSpace"]["SliceResolution"]
        expected = 1  # Instead of 1.0
        self.assertEqual(value, expected)

    def test_parse_float_conversion(self):
        instance_number = self.header.get("InstanceNumber")
        slice_position = self.parsed["SliceArray"]["Slice"][instance_number][
            "Position"
        ]["Tra"]
        expected = -58.1979682425
        self.assertEqual(slice_position, expected)

    def test_parse_cleans_extra_quotes(self):
        value = self.parsed["CoilSelectMeas"]["RxCoilSelectData"][0]["List"][0][
            "CoilElementID"
        ]["CoilID"]
        expected = "HeadNeck_64"
        self.assertEqual(value, expected)

    # TODO: Complete tests
