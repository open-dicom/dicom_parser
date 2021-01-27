from unittest import TestCase

from tests.fixtures import ChoiceEnumDefinition


class ChoiceEnumTestCase(TestCase):
    def test_choices_method(self):
        expected = ("A", "A"), ("B", "B"), ("C", "C")
        value = ChoiceEnumDefinition.choices()
        self.assertTupleEqual(value, expected)
