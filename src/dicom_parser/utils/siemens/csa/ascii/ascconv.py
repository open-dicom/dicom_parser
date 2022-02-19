# emacs: -*- mode: python-mode; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Parse the "ASCCONV" meta data format found in a variety of Siemens MR files.

Many Siemens files have a private data element that includes text, sandwiched
between ``### ASCCONV`` ``BEGIN`` and ``END`` lines.

Here are some example lines from that text::

    sGroupArray.lSize	 = 	1
    sGroupArray.anMember[1]	 = 	1
    sGroupArray.sPSat.ulShape	 = 	1
    sWipMemBlock.tFree	 = 	""WIP_Identifier: WIP#919B(Fri Feb 10 09:46:48 2017)""
    sWipMemBlock.alFree.__attribute__.size	 = 	64
    sWipMemBlock.alFree[0]	 = 	2
    sDiffusion.sFreeDiffusionData.sComment.0		 = 0x41    # 'A'

Notice that the names are in Hungarian-like notation, with a lower-case prefix
giving the object type (``s`` for Struct, ``a`` for Array, ``l`` for Long).
Notice too that we can't ignore these because variables may only differ in
their prefix, as in ``tFree`` and ``alFree`` above.

The ``ASCCONV`` text looks very much like standard Python assignment syntax,
with a few exceptions.  Specifically:

* The string quotes may or may not be doubled, as in ``""``, and as in the
  examples above.
* The last example line above is invalid Python syntax, because of the integer
  attribute name.

We deal with the first two exceptions by string replacements before parsing.

We can then parse the text with the Python AST parser.

The last problem for assignment is that lines like ``sWipMemBlock.alFree[0]	 =
2`` look like list assignment, but there may also be prior lines like
``sWipMemBlock.alFree.__attribute__.size = 64``, implying object assignment.

We deal with this by dropping any assignments containing ``__attribute__``.
"""  # noqa: E501
import ast
import re

from dicom_parser.utils.siemens.csa.ascii import messages

#: ASCCONV text block regular expression pattern.
ASCCONV_PATTERN = r"^### ASCCONV BEGIN((?:\s*[^=\s]+=[^=\s]+)*) ###\n(.*?)\n### ASCCONV END ###"  # noqa: E501

#: Regular expression to extract ASCCONV text block.
ASCCONV_RE = re.compile(ASCCONV_PATTERN, flags=re.M | re.S)

#: Terminal integer identifer regular expression pattern.
TERMINAL_DIGIT_PATTERN = r"^(.*)\.(\d+)(\s+=)"

#: Regular expression to replace terminal integer identifiers.
TERMINAL_DIGIT_RE = re.compile(TERMINAL_DIGIT_PATTERN, re.M)


class AscconvParseError(Exception):
    """
    Error parsing ascconv file.
    """


class NoValue:
    """
    Signals no value present.
    """


def assign_to_atoms(assign_ast, default_class=int):
    """
    Parse single assignment ast from ascconv line into atoms.

    Parameters
    ----------
    assign_ast : assignment statement ast
        ast derived from single line of ascconv file
    default_class : class, optional
        Class that will create an object where we cannot yet know the object
        type in the assignment

    Returns
    -------
    atoms : list
        List of length 3 tuples, where tuple values represent ``(target,
        obj_type, obj_id)``.  Defines left to right sequence of assignment in
        `line_ast`
    """
    n_targets = len(assign_ast.targets)
    if not n_targets == 1:
        message = messages.AST_N_TARGETS.format(n_targets=n_targets)
        raise AscconvParseError(message)
    target = assign_ast.targets[0]
    atoms = []
    prev_target_type = default_class  # Placeholder for any scalar value
    while True:
        if isinstance(target, ast.Name):
            atoms.append((target, prev_target_type, target.id))
            break
        if isinstance(target, ast.Attribute):
            atoms.append((target, prev_target_type, target.attr))
            target = target.value
            prev_target_type = dict
        elif isinstance(target, ast.Subscript):
            if isinstance(target.slice, ast.Constant):  # PY39
                index = target.slice.n
            else:  # PY38
                index = target.slice.value.n
            atoms.append((target, prev_target_type, index))
            target = target.value
            prev_target_type = list
        else:
            message = messages.UNEXPECTED_LHS.format(target=target)
            raise AscconvParseError(message)
    return atoms[::-1]


def _create_obj_in(maker, name, root):
    """
    Find or create object `maker` in dict-like `root` with given `name`.

    Returns corresponding value if there is already a key matching `name` in
    `root`. Otherwise, create new object with `maker`, insert into dictionary,
    and return new object.

    Can therefore modify `root` in place.
    """
    obj = root.get(name, NoValue)
    if obj is not NoValue:
        return obj
    obj = maker()
    root[name] = obj
    return obj


def _create_subscript_in(maker, index, root):
    """
    Find or create and insert object of type `maker` in `root` at `index`.

    If `root` is long enough to contain this `index`, return the object at that
    index.  Otherwise, extend `root` with None elements to contain index
    `index`, then create a new object by calling `maker`, insert at the end of
    the list, and return this object.

    Can therefore modify `root` in place.
    """
    curr_n = len(root)
    if curr_n > index:
        return root[index]
    obj = maker()
    root += [None] * (index - curr_n) + [obj]
    return obj


def obj_from_atoms(atoms, namespace):
    """
    Return object defined by list `atoms` in dict-like `namespace`.

    Parameters
    ----------
    atoms : Iterable
        Iterable of atoms, where atoms are length 3 tuples of (target,
        obj_type, obj_id)
    namespace : dict-like
        Namespace in which object will be defined

    Returns
    -------
    obj_root : object
        Namespace such that we can set a desired value to the object defined in
        `atoms` with ``obj_root[obj_key] = value``.  `None` signals that the
        function wants to discard this assignment
    obj_key : str or int or None
        Index into list or key into dictionary for `obj_root`.  If function
        rejects assignment, and `obj_root` is None, `obj_key` should be `None`
    """
    root_obj = namespace
    atoms = list(atoms)
    # Discard __attribute__ lines.
    if any(e for e in atoms if e[2] == "__attribute__"):
        return None, None
    for el in atoms:
        prev_root = root_obj
        target, maker, name = el
        if isinstance(target, (ast.Attribute, ast.Name)):
            root_obj = _create_obj_in(maker, name, root_obj)
        elif isinstance(target, ast.Subscript):
            root_obj = _create_subscript_in(maker, name, root_obj)
        else:
            message = messages.UNEXPECTED_TARGET.format(target=target, el=el)
            raise AscconvParseError(message)
        if not isinstance(root_obj, maker):
            message = messages.BAD_ASCCONV_TYPE.format(
                el=el, maker=maker, expected_type=type(root_obj)
            )
            raise AscconvParseError(message)
    return prev_root, name


def _get_value(assign):
    value = assign.value
    if isinstance(value, ast.Num):
        return value.n
    if isinstance(value, ast.Str):
        return value.s
    if isinstance(value, ast.UnaryOp) and isinstance(value.op, ast.USub):
        return -value.operand.n
    message = messages.UNEXPECTED_RHS.format(value=value)
    raise AscconvParseError(message)


def parse_ascconv_text(content, delimiter='"'):
    """
    Parse ASCCONV text format from `content` string.

    Parameters
    ----------
    content : str
        The string we are parsing
    delimiter : str, optional
        String delimiter.  Typically '"' or '""'

    Returns
    -------
    prot_dict : dict
        Meta data pulled from the ASCCONV section
    attrs : dict
        Any attributes stored in the 'ASCCONV BEGIN' line

    Raises
    ------
    AsconvParseError
        A line of the ASCCONV section could not be parsed
    """
    # Normalize string start / end markers to something Python understands
    content = content.replace(delimiter, '"""').replace("\\", "\\\\")
    # Invalid digit identifiers to list
    content = TERMINAL_DIGIT_RE.sub(r"\1[\2]\3", content)
    # Use Python's own parser to parse modified ASCCONV assignments
    tree = ast.parse(content)

    prot_dict = {}
    for assign in tree.body:
        atoms = assign_to_atoms(assign)
        obj_to_index, key = obj_from_atoms(atoms, prot_dict)
        if obj_to_index is not None:  # None if obj_from_atoms rejected atoms.
            obj_to_index[key] = _get_value(assign)
    return prot_dict


def parse_ascconv(ascconv_str: str, delimiter: str = '"'):
    """
    Extract and parse the ASCCONV format from `ascconv_str`.

    Parameters
    ----------
    ascconv_str : str
        The string we are parsing
    delimiter : str, optional
        String delimiter.  Typically '"' or '""'

    Returns
    -------
    prot_dict : dict
        Meta data pulled from the ASCCONV section
    attrs : dict
        Any attributes stored in the 'ASCCONV BEGIN' line

    Raises
    ------
    AsconvParseError
        A line of the ASCCONV section could not be parsed
    """
    attrs, content = ASCCONV_RE.search(ascconv_str).groups()
    attrs = dict((tuple(x.split("=")) for x in attrs.split()))
    return parse_ascconv_text(content, delimiter), attrs
