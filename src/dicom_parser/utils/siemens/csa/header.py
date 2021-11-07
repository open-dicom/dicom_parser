"""
Definition of the :class:`CsaHeader` class.
"""
from typing import Any, Iterable

from dicom_parser.utils.siemens.csa.ascii import CsaAsciiHeader
from dicom_parser.utils.siemens.csa.exceptions import CsaReadError
from dicom_parser.utils.siemens.csa.messages import (
    INVALID_CHECK_BIT,
    READ_OVERREACH,
)
from dicom_parser.utils.siemens.csa.unpacker import Unpacker
from dicom_parser.utils.siemens.csa.utils import VR_TO_TYPE, strip_to_null


class CsaHeader:
    """
    Represents a full CSA header data element, i.e. either
    (0029, 1010)/`"CSA Image Header Info"` or (0029, 1020)/`"CSA Series Header
    Info"`, and provides access to the header as a parsed dictionary.
    This implementation is heavily based on `dicom2nifti`_'s code
    (particularly `this module`_).

    .. _dicom2nifti:
       https://github.com/icometrix/dicom2nifti
    .. _this module:
       https://github.com/icometrix/dicom2nifti/blob/6722420a7673d36437e4358ce3cb2a7c77c91820/dicom2nifti/convert_siemens.py#L342
    """

    CSA_TYPE_1: int = 1
    CSA_TYPE_2: int = 2

    #: Used to determine whether the CSA header is of type 1 or 2.
    TYPE_2_IDENTIFIER: bytes = b"SV10"

    #: Endian format used to parse the CSA header information (little-endian).
    ENDIAN: str = "<"

    #: Format string used to unpack a single tag.
    TAG_FORMAT_STRING: str = "64si4s3i"

    #: Number of tags unpacking format characters (2 unsigned integers).
    PREFIX_FORMAT: str = "2I"

    #: Item value unpacking format characters (4 integers).
    ITEM_FORMAT: str = "4i"

    #: Valid values for the CSA element's check bit.
    VALID_CHECK_BIT_VALUES: Iterable[int] = {77, 205}

    #: ASCII header tag names.
    ASCII_HEADER_TAGS: Iterable[str] = {"MrPhoenixProtocol"}

    #: CSA type 1 length fix.
    _first_tag_n_items: int = None

    def __init__(self, raw: bytes):
        """
        Initialize a new `CsaHeader` instance.

        Parameters
        ----------
        raw : bytes
            Raw CSA header as read by *pydicom*
        """
        self.raw = raw
        self.header_size = len(self.raw)

    def skip_prefix(self, unpacker: Unpacker):
        """
        Skip the CSA type 2 header prefix.

        See Also
        --------
        * :attr:`TYPE_2_IDENTIFIER`

        Parameters
        ----------
        unpacker : Unpacker
            Stream-like header reader
        """
        if self.is_type_2:
            prefix_length = len(self.TYPE_2_IDENTIFIER)
            unpacker.pointer = prefix_length
            unpacker.read(prefix_length)

    def validate_check_bit(self, i_tag: int, value: int):
        """
        Validates a single CSA header tag's check-bit.

        See Also
        --------
        * :attr:`VALID_CHECK_BIT_VALUES`

        Parameters
        ----------
        i_tag : int
            Index of the parsed tag
        value : int
            Check-bit value

        Raises
        ------
        CsaReadError
            Invalid check-bit value
        """
        if value not in self.VALID_CHECK_BIT_VALUES:
            message = INVALID_CHECK_BIT.format(
                i_tag=i_tag,
                check_bit=value,
                valid_values=self.VALID_CHECK_BIT_VALUES,
            )
            raise CsaReadError(message)

    def parse_items(
        self, unpacker: Unpacker, n_items: int, vr: str, vm: int
    ) -> Any:
        """
        Parses a single header element's value.

        Parameters
        ----------
        unpacker : Unpacker
            Stream-like header reader
        n_items : int
            Number of items in this element's value as described in the header
            information
        vr : str
            Value representation
        vm : int
            Value multiplicity

        Returns
        -------
        Any
            CSA header element value

        Raises
        ------
        CsaReadError
            Invalid element value
        """
        n_values = vm or n_items
        converter = VR_TO_TYPE.get(vr)
        items = []
        for i_item in range(n_items):
            x0, x1, _, _ = unpacker.unpack(self.ITEM_FORMAT)
            # CSA1 odd length calculation
            if self.csa_type == 1:
                item_len = x0 - self._first_tag_n_items
                destination = unpacker.pointer + item_len
                negative_length = item_len < 0
                overreach = destination > self.header_size
                if negative_length or overreach:
                    if i_item < vm:
                        items.append("")
                    break
            # CSA2
            else:
                item_len = x1
                destination = unpacker.pointer + item_len
                if destination > self.header_size:
                    message = READ_OVERREACH.format(
                        destination=destination, max_length=self.header_size
                    )
                    raise CsaReadError(message)
            if i_item >= n_values:
                assert item_len == 0
                continue
            item = strip_to_null(unpacker.read(item_len))
            if converter:
                # We may have fewer real items than are given in
                # n_items, but we don't know how many - assume that
                # we've reached the end when we hit an empty item
                if item_len == 0:
                    n_values = i_item
                    continue
                item = converter(item)
            items.append(item)
            # go to 4 byte boundary
            remainder = item_len % 4
            if remainder != 0:
                unpacker.pointer += 4 - remainder
        if items:
            return items if len(items) > 1 else items.pop()

    def parse_tag(self, unpacker: Unpacker, i_tag: int) -> dict:
        # 4th element (SyngoDT) seems to be a numeric representation of the
        # datatype, which is already provided as the VR.
        name, vm, vr, _, n_items, check_bit = unpacker.unpack(
            self.TAG_FORMAT_STRING
        )
        self.validate_check_bit(i_tag, check_bit)
        name = strip_to_null(name)
        vr = strip_to_null(vr)
        tag = {
            "name": name,
            "index": i_tag,
            "VR": vr,
            "VM": vm,
        }
        # CSA1-specific length modifier
        if i_tag == 1:
            self._first_tag_n_items = n_items
        tag["value"] = self.parse_items(unpacker, n_items, vr, vm)
        if name in self.ASCII_HEADER_TAGS:
            tag["value"] = CsaAsciiHeader(tag["value"]).parse()
        return tag

    def read(self) -> dict:
        unpacker = Unpacker(self.raw, endian=self.ENDIAN)
        self.skip_prefix(unpacker)
        n_tags, _ = unpacker.unpack(self.PREFIX_FORMAT)
        result = {}
        for i_tag in range(n_tags):
            tag = self.parse_tag(unpacker, i_tag)
            name = tag.pop("name")
            result[name] = tag
        return result

    def check_csa_type(self) -> int:
        """
        Checks whether the given CSA header is of type 1 or 2.

        See Also
        --------
        * :func:`csa_type`

        Returns
        -------
        int
            CSA header type (1 or 2)
        """
        is_type_2 = self.raw[:4] == self.TYPE_2_IDENTIFIER
        return self.CSA_TYPE_2 if is_type_2 else self.CSA_TYPE_1

    @property
    def csa_type(self) -> int:
        """
        Checks whether the given CSA header is of type 1 or 2.

        See Also
        --------
        * :func:`check_csa_type`

        Returns
        -------
        int
            CSA header type (1 or 2)
        """
        return self.check_csa_type()

    @property
    def is_type_2(self) -> bool:
        """
        Returns whether this header if CSA type 2 or not (1).

        Returns
        -------
        bool
            CSA type 2 or not
        """
        return self.csa_type == self.CSA_TYPE_2
