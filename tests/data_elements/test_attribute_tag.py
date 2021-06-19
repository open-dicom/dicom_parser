"""
Definition of the :class:`AttributeTagTestCase` class.
"""
from dicom_parser.data_elements.attribute_tag import AttributeTag
from tests.test_data_element import DataElementTestCase


class AttributeTagTestCase(DataElementTestCase):
    """
    Tests for the
    :class:`~dicom_parser.data_elements.attribute_tag.AttributeTag`
    class.
    """

    TEST_CLASS = AttributeTag
