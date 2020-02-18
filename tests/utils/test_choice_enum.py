from dicom_parser.utils.choice_enum import ChoiceEnum
from unittest import TestCase


class TestEnum(ChoiceEnum):
    A = "A"
    B = "B"
    C = "C"


class ChoiceEnumTestCase(TestCase):
    def test_choices_method(self):
        expected = ("A", "A"), ("B", "B"), ("C", "C")
        value = TestEnum.choices()
        self.assertTupleEqual(value, expected)
