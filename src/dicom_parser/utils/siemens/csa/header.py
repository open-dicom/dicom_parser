from dicom_parser.utils.siemens.csa.unpacker import Unpacker
from dicom_parser.utils.siemens.csa.utils import strip_to_null, VR_TO_TYPE
from dicom_parser.utils.siemens.csa.exceptions import CsaReadError


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

    #: Used to determine whether the CSA header is of type 1 or 2.
    TYPE_2_IDENTIFIER: bytes = b"SV10"

    #: Endian format used to parse the CSA header information (little-endian).
    ENDIAN: str = "<"

    #: Format string used to unpack a single tag.
    TAG_FORMAT_STRING: str = "64si4s3i"

    #: Number of tags unpacking format characters (2 unsigned integers).
    PREFIX_FORMAT: str = "2I"

    def __init__(self, raw: bytes):
        self.raw = raw

    def read(self) -> dict:
        unpacker = Unpacker(self.raw, endian=self.ENDIAN)
        if self.csa_type == 2:
            unpacker.pointer = 4
            unpacker.read(4)
        n_tags, _ = unpacker.unpack(self.PREFIX_FORMAT)
        result = {}
        for i_tag in range(n_tags):
            name, vm, vr, syngodt, n_items, last3 = unpacker.unpack(
                self.TAG_FORMAT_STRING
            )
            name = strip_to_null(name)
            vr = strip_to_null(vr)
            tag = {
                "n_items": n_items,
                "vm": vm,
                "vr": vr,
                "syngodt": syngodt,
                "last3": last3,
                "i_tag": i_tag,
            }
            n_values = vm if vm != 0 else n_items
            converter = VR_TO_TYPE.get(vr)
            # CSA1-specific length modifier
            if i_tag == 1:
                tag0_n_items = n_items
            items = []
            for i_item in range(n_items):
                x0, x1, x2, x3 = unpacker.unpack("4i")
                pointer = unpacker.pointer
                if self.csa_type == 1:  # CSA1 - odd length calculation
                    item_len = x0 - tag0_n_items
                    if item_len < 0 or (pointer + item_len) > len(self.raw):
                        if i_item < vm:
                            items.append("")
                        break
                else:  # CSA2
                    item_len = x1
                    if (pointer + item_len) > len(self.raw):
                        raise CsaReadError("Item is too long, aborting read!")
                if i_item >= n_values:
                    assert item_len == 0
                    continue
                item = strip_to_null(unpacker.read(item_len))
                if converter:
                    # we may have fewer real items than are given in
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
            tag["items"] = items
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
        return 2 if self.raw[:4] == self.TYPE_2_IDENTIFIER else 1

    @property
    def csa_type(self) -> int:
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
        return self.check_csa_type()
