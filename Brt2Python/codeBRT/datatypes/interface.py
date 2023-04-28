# -*- coding: utf-8 -*-
"""
@author: Steven
"""
from abc import ABC, abstractmethod


class IDataType(ABC):
    """ The interface for property data types. """

    @abstractmethod
    def is_type_of(self, obj):
        """
        The public method which needs to call upon raw_is_type_of.

        Args:
            obj: Whatever possible object you want to test.

        Returns: whether this given object (obj) is of data type.

        """

    @abstractmethod
    def raw_is_type_of(self, obj):
        """
        Args:
            obj: Whatever possible object you want to test.

        Returns: whether this given object (obj) is of data type.

        This method should be defined specifically for each data type.
        """

    @abstractmethod
    def serialize(self, obj):
        """

        Args:
            obj: An object, hinted to be an instance of the data type
                defined by self.

        Returns: A byte array serialization of this object.

        """

    @abstractmethod
    def deserialize(self, str_repr):
        """

        Args:
            str_repr: A byte array serialization of an object.

        Returns: The original object.

        """


