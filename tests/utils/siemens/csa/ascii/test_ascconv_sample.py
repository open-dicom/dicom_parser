"""
Tests for the the Siemens "ASCCONV" parser.
"""

import ast
from collections import OrderedDict

import pytest
from dicom_parser.utils.siemens.csa.ascii.ascconv import (
    AscconvParseError,
    assign_to_atoms,
    obj_from_atoms,
    parse_ascconv,
    parse_ascconv_text,
)
from numpy.testing import assert_array_almost_equal, assert_array_equal
from tests.fixtures import TEST_ASCCONV_SAMPLE


def test_ascconv_parse():
    with open(TEST_ASCCONV_SAMPLE, "rt") as fobj:
        contents = fobj.read()
    ascconv_dict, attrs = parse_ascconv(contents, delimiter='""')
    assert attrs == OrderedDict()
    assert len(ascconv_dict) == 72
    assert ascconv_dict["tProtocolName"] == "CBU+AF8-DTI+AF8-64D+AF8-1A"
    assert ascconv_dict["ucScanRegionPosValid"] == 1
    assert_array_almost_equal(
        ascconv_dict["sProtConsistencyInfo"]["flNominalB0"], 2.89362
    )
    assert ascconv_dict["sProtConsistencyInfo"]["flGMax"] == 26
    assert list(ascconv_dict["sSliceArray"].keys()) == [
        "asSlice",
        "anAsc",
        "anPos",
        "lSize",
        "lConc",
        "ucMode",
        "sTSat",
    ]
    slice_arr = ascconv_dict["sSliceArray"]
    as_slice = slice_arr["asSlice"]
    assert_array_equal([e["dPhaseFOV"] for e in as_slice], 230)
    assert_array_equal([e["dReadoutFOV"] for e in as_slice], 230)
    assert_array_equal([e["dThickness"] for e in as_slice], 2.5)
    # Some lists defined starting at 1, so have None as first element
    assert slice_arr["anAsc"] == [None] + list(range(1, 48))
    assert slice_arr["anPos"] == [None] + list(range(1, 48))
    # A top level list
    assert len(ascconv_dict["asCoilSelectMeas"]) == 1
    as_list = ascconv_dict["asCoilSelectMeas"][0]["asList"]
    # This lower-level list does start indexing at 0
    assert len(as_list) == 12
    for i, el in enumerate(as_list):
        assert list(el.keys()) == [
            "sCoilElementID",
            "lElementSelected",
            "lRxChannelConnected",
        ]
        assert el["lElementSelected"] == 1
        assert el["lRxChannelConnected"] == i + 1
    # Test negative number
    assert_array_almost_equal(as_slice[0]["sPosition"]["dCor"], -20.03015269)


def test_ascconv_w_attrs():
    in_str = (
        "### ASCCONV BEGIN object=MrProtDataImpl@MrProtocolData "
        "version=41340006 "
        "converter=%MEASCONST%/ConverterList/Prot_Converter.txt ###\n"
        'test = "hello"\n'
        "### ASCCONV END ###"
    )
    ascconv_dict, attrs = parse_ascconv(in_str, '""')
    assert attrs["object"] == "MrProtDataImpl@MrProtocolData"
    assert attrs["version"] == "41340006"
    assert attrs["converter"] == "%MEASCONST%/ConverterList/Prot_Converter.txt"
    assert ascconv_dict["test"] == "hello"


def test_drop_attributes():
    in_text = """\
sWipMemBlock.alFree.__attribute__.size	 = 	64
sWipMemBlock.alFree[0]	 = 	2
sWipMemBlock.alFree[4]	 = 	1
sWipMemBlock.alFree[5]	 = 	1
"""
    out = parse_ascconv_text(in_text)
    assert out == {"sWipMemBlock": {"alFree": [2, None, None, None, 1, 1]}}


def atom_seq_same(seq1, seq2):
    if len(seq1) != len(seq2):
        return False
    for a1, a2 in zip(seq1, seq2):
        if (
            not isinstance(a1[0], type(a2[0]))
            or a1[1] != a2[1]
            or a1[2] != a2[2]
        ):
            return False
    return True


def test_assign_to_atoms():
    assign = ast.parse("foo = 64").body[0]
    atoms = assign_to_atoms(assign)
    assert atom_seq_same(atoms, [(ast.Name(), int, "foo")])
    assign = ast.parse("foo.bar.baz = 64").body[0]
    atoms = assign_to_atoms(assign)
    assert atom_seq_same(
        atoms,
        [
            (ast.Name(), dict, "foo"),
            (ast.Attribute(), dict, "bar"),
            (ast.Attribute(), int, "baz"),
        ],
    )
    assign = ast.parse("foo[0].bar.baz = 64").body[0]
    atoms = assign_to_atoms(assign)
    assert atom_seq_same(
        atoms,
        [
            (ast.Name(), list, "foo"),
            (ast.Subscript(), dict, 0),
            (ast.Attribute(), dict, "bar"),
            (ast.Attribute(), int, "baz"),
        ],
    )
    # Can set the default type.
    atoms = assign_to_atoms(assign, default_class=list)
    assert atom_seq_same(
        atoms,
        [
            (ast.Name(), list, "foo"),
            (ast.Subscript(), dict, 0),
            (ast.Attribute(), dict, "bar"),
            (ast.Attribute(), list, "baz"),
        ],
    )
    assign = ast.parse("foo, bar = 1, 2").body[0]
    with pytest.raises(AscconvParseError):
        assign_to_atoms(assign)


def test_parse_attribute_return():
    in_text = "foo.bar.baz = 64"
    assign = ast.parse(in_text).body[0]
    atoms = assign_to_atoms(assign)
    assert obj_from_atoms(atoms, {}) == ({"baz": 0}, "baz")
    # Attribute anywhere returns None, None
    assign = ast.parse("foo.bar.__attribute__ = 64").body[0]
    atoms = assign_to_atoms(assign)
    assert obj_from_atoms(atoms, {}) == (None, None)
    assign = ast.parse("foo.__attribute__.bar = 64").body[0]
    atoms = assign_to_atoms(assign)
    assert obj_from_atoms(atoms, {}) == (None, None)


def test_replace_end_digits():
    in_text = """\
sComment.0		 = 0x41    # 'A'
sComment.1		 = 0x78    # 'x'
sComment.2		 = 0x43    # 'C'
sComment.3		 = 0x61    # 'a'
"""
    out = parse_ascconv_text(in_text)
    assert out == {"sComment": [0x41, 0x78, 0x43, 0x61]}


def test_some_errors():
    in_text = """\
foo.bar[0] = 1
foo.bar[1] = 2
"""
    out = parse_ascconv_text(in_text)
    assert out == {"foo": {"bar": [1, 2]}}
    list_then_dict = """\
foo.bar[0] = 1
foo.bar.baz = 2
"""
    with pytest.raises(AscconvParseError):
        out = parse_ascconv_text(list_then_dict)
    dict_then_list = """\
foo.bar.baz = 2
foo.bar[0] = 1
"""
    with pytest.raises(AscconvParseError):
        out = parse_ascconv_text(dict_then_list)
    val_then_list = """\
foo.bar = 2
foo.bar[0] = 1
"""
    with pytest.raises(AscconvParseError):
        out = parse_ascconv_text(val_then_list)
