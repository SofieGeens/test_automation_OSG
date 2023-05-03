# -*- coding: utf-8 -*-
import struct
from abc import ABC, abstractmethod


class Component(ABC):
    """
    Any identifiable structure in a BrainRT datafile.
    """

    @property
    @abstractmethod
    def type_string(self):
        """
        String determining the format parsed by "struct" functionality.
        Possible combinations are defined in the python docs.
        """

    @classmethod
    def parse(cls, byte_code: bytes):
        """
        Constructs an object belonging to this class from the byte_code.
        This is a direct call to the struct parser.

        Args:
            byte_code: byte representation of the object

        Returns:
            Instance of this class
        """
        struct_representation = struct.unpack(cls.type_string, byte_code)
        result = cls(*struct_representation)
        return result

    @staticmethod
    def parse_wchar(byte_code: bytes) -> str:
        """
        Special parser for the C++ wide character data type.
        This does not parse any other data type.

        Args:
            byte_code: byte representation of a string of wide characters

        Returns:
            python string
        """

        terminator = 0
        while terminator < len(byte_code):
            if byte_code[terminator: terminator + 2] == bytes(2):
                break
            terminator += 2
        byte_code = byte_code[:terminator]
        return byte_code.decode('utf-16')

    @classmethod
    def parse_from(cls, handle):
        """
        Reads an instance from an open handle.
        This function is not responsible for closing the handle,
        as it did not open it.

        Args:
            handle: IO handle of a file, implementing a "read(bytes)" function

        Returns:
            Instance of this class
        """
        n_bytes = cls.size()
        data = handle.read(n_bytes)
        content = cls.parse(data)
        return content

    @classmethod
    def size(cls) -> int:
        """
        Integer representing the number of bytes which represent this component.

        Returns:
            size of this class in bytes
        """
        return struct.calcsize(cls.type_string)