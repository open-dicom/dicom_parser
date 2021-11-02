"""
Based on NiBabel's `nicom` module.

References
----------
* https://github.com/nipy/nibabel/blob/4703f4d8e32be4cec30e829c2d93ebe54759bb62/nibabel/nicom/structreader.py # noqa: E501
"""
from struct import Struct

#: Valid Endian codes.
ENDIAN_CODES = "@=<>!"


class Unpacker(object):
    """
    Class to unpack values from buffer object.

    The buffer object is usually a string. Caches compiled :mod:`struct`
    format strings so that repeated unpacking with the same format
    string should be faster than using ``struct.unpack`` directly.

    Examples
    --------
    >>> a = b'1234567890'
    >>> upk = Unpacker(a)
    >>> upk.unpack('2s') == (b'12',)
    True
    >>> upk.unpack('2s') == (b'34',)
    True
    >>> upk.ptr
    4
    >>> upk.read(3) == b'567'
    True
    >>> upk.ptr
    7
    """

    def __init__(self, buffer, pointer: int = 0, endian: str = None):
        """
        Initialize unpacker instance.

        Parameters
        ----------
        buf : buffer
           Object implementing buffer protocol (e.g. str)
        ptr : int, optional
           Offset at which to begin reads from `buf`
        endian : None or str, optional
           Endian code to prepend to format, as for ``unpack`` endian
           codes.  None (the default) corresponds to the default
           behavior of ``struct`` - assuming system endian unless you
           specify the byte order specifically in the format string
           passed to ``unpack``
        """
        self.buffer = buffer
        self.pointer = pointer
        self.endian = endian
        self._cache = {}

    def unpack(self, format_string):
        """
        Unpack values from contained buffer.

        Unpacks values from ``self.buffer`` and updates ``self.pointer`` to the
        position after the read data.

        Parameters
        ----------
        format_string : str
           Format string as for ``unpack``

        Returns
        -------
        values : tuple
           Values as unpacked from ``self.buffer`` according to `format_string`
        """
        # Try and get a struct corresponding to the format string from
        # the cache.
        packed_struct = self._cache.get(format_string)
        if packed_struct is None:  # struct not in cache
            # if we've not got a default endian, or the format has an
            # explicit endianness, then we make a new struct directly
            # from the format string
            if self.endian is None or format_string[0] in ENDIAN_CODES:
                packed_struct = Struct(format_string)
            else:  # we're going to modify the endianness with our
                # default.
                endian_format_string = self.endian + format_string
                packed_struct = Struct(endian_format_string)
                # add an entry in the cache for the modified format
                # string as well as (below) the unmodified format
                # string, in case we get a format string with the same
                # endianness as default, but specified explicitly.
                self._cache[endian_format_string] = packed_struct
            self._cache[format_string] = packed_struct
        values = packed_struct.unpack_from(self.buffer, self.pointer)
        self.pointer += packed_struct.size
        return values

    def read(self, n_bytes: int = -1):
        """
        Return byte string of length `n_bytes` at current position.

        Returns sub-string from ``self.buffer`` and updates ``self.pointer`` to the
        position after the read data.

        Parameters
        ----------
        n_bytes : int, optional
           Number of bytes to read. Can be -1 (the default) in which
           case we return all the remaining bytes in ``self.buffer``

        Returns
        -------
        s : byte string
        """
        start = self.pointer
        end = len(self.buffer) if n_bytes == -1 else start + n_bytes
        self.pointer = end
        return self.buffer[start:end]
