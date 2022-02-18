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
"""

import re
import ast

#: Regular expression to extract ASCCONV text block.
ASCCONV_RE = re.compile(
    r'^### ASCCONV BEGIN((?:\s*[^=\s]+=[^=\s]+)*) ###\n(.*?)\n### ASCCONV END ###',
    flags=re.M | re.S)

#: Regular expression to replace terminal integer identifiers.
_TERM_DIGIT_RE = re.compile(r'^(.*)\.(\d+)(\s+=)', re.M)


class AscconvParseError(Exception):
    """ Error parsing ascconv file """


class Atom:
    """ Object to hold operation, object type and object identifier

    An atom represents an element in an expression.  For example::

        a.b[0].c

    has four elements.  We call these elements "atoms".

    We represent objects (like ``a``) as dicts for convenience.

    The last element (``.c``) is an ``op = ast.Attribute`` operation where the
    object type (`obj_type`) of ``c`` is not constrained (we can't tell from
    the operation what type it is).  The `obj_id` is the name of the object --
    "c".

    The second to last element ``[0]``, is ``op = ast.Subscript``, with object type
    dict (we know from the subsequent operation ``.c`` that this must be an
    object, we represent the object by a dict).  The `obj_id` is the index 0.

    Parameters
    ----------
    op : {'name', 'attr', 'list'}
        Assignment type.  Assignment to name (root namespace), attribute or
        list element.
    obj_type : {list, dict, other}
        Object type being assigned to.
    obj_id : str or int
        Key (``obj_type is dict``) or index (``obj_type is list``)
    """

    def __init__(self, op, obj_type, obj_id):
        self.op = op
        self.obj_type = obj_type
        self.obj_id = obj_id


class NoValue:
    """ Signals no value present """


def assign2atoms(assign_ast, default_class=int):
    """ Parse single assignment ast from ascconv line into atoms

    Parameters
    ----------
    assign_ast : assignment statement ast
        ast derived from single line of ascconv file.
    default_class : class, optional
        Class that will create an object where we cannot yet know the object
        type in the assignment.

    Returns
    -------
    atoms : list
        List of :class:`atoms`.  See docstring for :class:`atoms`.  Defines
        left to right sequence of assignment in `line_ast`.
    """
    if not len(assign_ast.targets) == 1:
        raise AscconvParseError('Too many targets in assign')
    target = assign_ast.targets[0]
    atoms = []
    prev_target_type = default_class  # Placeholder for any scalar value
    while True:
        if isinstance(target, ast.Name):
            atoms.append(Atom(target, prev_target_type, target.id))
            break
        if isinstance(target, ast.Attribute):
            atoms.append(Atom(target, prev_target_type, target.attr))
            target = target.value
            prev_target_type = dict
        elif isinstance(target, ast.Subscript):
            if isinstance(target.slice, ast.Constant):  # PY39
                index = target.slice.n
            else:  # PY38
                index = target.slice.value.n
            atoms.append(Atom(target, prev_target_type, index))
            target = target.value
            prev_target_type = list
        else:
            raise AscconvParseError(f'Unexpected LHS element {target}')
    return reversed(atoms)


def _create_obj_in(atom, root):
    """ Find / create object defined in `atom` in dict-like given by `root`

    Returns corresponding value if there is already a key matching
    `atom.obj_id` in `root`.

    Otherwise, create new object with ``atom.obj_type`, insert into dictionary,
    and return new object.

    Can therefore modify `root` in place.
    """
    name = atom.obj_id
    obj = root.get(name, NoValue)
    if obj is not NoValue:
        return obj
    obj = atom.obj_type()
    root[name] = obj
    return obj


def _create_subscript_in(atom, root):
    """ Find / create and insert object defined by `atom` from list `root`

    The `atom` has an index, defined in ``atom.obj_id``.  If `root` is long
    enough to contain this index, return the object at that index.  Otherwise,
    extend `root` with None elements to contain index ``atom.obj_id``, then
    create a new object via ``atom.obj_type()``, insert at the end of the list,
    and return this object.

    Can therefore modify `root` in place.
    """
    curr_n = len(root)
    index = atom.obj_id
    if curr_n > index:
        return root[index]
    obj = atom.obj_type()
    root += [None] * (index - curr_n) + [obj]
    return obj


class TrashValue:
    """ Indicates useless value from parsing assignment """


def obj_from_atoms(atoms, namespace):
    """ Return object defined by list `atoms` in dict-like `namespace`

    Parameters
    ----------
    atoms : list
        List of :class:`atoms`
    namespace : dict-like
        Namespace in which object will be defined.

    Returns
    -------
    obj_root : object
        Namespace such that we can set a desired value to the object defined in
        `atoms` with ``obj_root[obj_key] = value``.
    obj_key : str or int
        Index into list or key into dictionary for `obj_root`.
    """
    root_obj = namespace
    atoms = list(atoms)
    # Discard __attribute__ lines.
    if any(e for e in atoms if e.obj_id == '__attribute__' ):
        return TrashValue, TrashValue
    for el in atoms:
        prev_root = root_obj
        if isinstance(el.op, (ast.Attribute, ast.Name)):
            root_obj = _create_obj_in(el, root_obj)
        else:
            root_obj = _create_subscript_in(el, root_obj)
        if not isinstance(root_obj, el.obj_type):
            raise AscconvParseError(
                f'{el.obj_id} has type {el.obj_type}, but expecting '
                f'type {type(root_obj)}')
    return prev_root, el.obj_id


def _get_value(assign):
    value = assign.value
    if isinstance(value, ast.Num):
        return value.n
    if isinstance(value, ast.Str):
        return value.s
    if isinstance(value, ast.UnaryOp) and isinstance(value.op, ast.USub):
        return -value.operand.n
    raise AscconvParseError(f'Unexpected RHS of assignment: {value}')


def parse_ascconv_text(content, str_delim='"'):
    '''Parse ASCCONV text format from `content` string.

    Parameters
    ----------
    content : str
        The string we are parsing
    str_delim : str, optional
        String delimiter.  Typically '"' or '""'

    Returns
    -------
    prot_dict : dict
        Meta data pulled from the ASCCONV section.
    attrs : dict
        Any attributes stored in the 'ASCCONV BEGIN' line

    Raises
    ------
    AsconvParseError
        A line of the ASCCONV section could not be parsed.
    '''
    # Normalize string start / end markers to something Python understands
    content = content.replace(str_delim, '"""').replace("\\", "\\\\")
    # Invalid digit identifiers to list
    content = _TERM_DIGIT_RE.sub(r'\1[\2]\3', content)
    # Use Python's own parser to parse modified ASCCONV assignments
    tree = ast.parse(content)

    prot_dict = {}
    for assign in tree.body:
        atoms = assign2atoms(assign)
        obj_to_index, key = obj_from_atoms(atoms, prot_dict)
        if key is not TrashValue:  # Function may have discarded line.
            obj_to_index[key] = _get_value(assign)
    return prot_dict


def parse_ascconv(ascconv_str, str_delim='"'):
    '''Extract and parse the 'ASCCONV' format from `input_str`.

    Parameters
    ----------
    ascconv_str : str
        The string we are parsing
    str_delim : str, optional
        String delimiter.  Typically '"' or '""'

    Returns
    -------
    prot_dict : dict
        Meta data pulled from the ASCCONV section.
    attrs : dict
        Any attributes stored in the 'ASCCONV BEGIN' line

    Raises
    ------
    AsconvParseError
        A line of the ASCCONV section could not be parsed.
    '''
    attrs, content = ASCCONV_RE.search(ascconv_str).groups()
    attrs = dict((tuple(x.split('=')) for x in attrs.split()))
    return parse_ascconv_text(content, str_delim), attrs
