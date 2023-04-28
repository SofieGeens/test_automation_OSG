# -*- coding: utf-8 -*-
from sklearn.ensemble import RandomForestClassifier

from codeBRT.datatypes.base import PickleBase


class RFClassifierTypeClass(PickleBase):
    """
    The class generating the datatype for a random forest classifier

    See Base class for serialization and deserialization.
    """

    def raw_is_type_of(self, obj):
        return isinstance(obj, RandomForestClassifier)


RFClassifierType = RFClassifierTypeClass()
