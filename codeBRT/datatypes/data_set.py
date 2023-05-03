import os

import pandas as pd

from blocks.data.data_set import DataSet
from codeBRT.datatypes.interface import IDataType
from definitions import path_parameters

all_measurements = pd.read_csv(os.path.join(path_parameters,
                                            'all_measurements.csv'))


class _data_set_type(IDataType):
    """
    DataType for all datasets.
    The set of indices is directly serialized as flags.
    """
    pass

    def is_type_of(self, obj):
        return isinstance(obj, DataSet)

    def raw_is_type_of(self, obj):
        return isinstance(obj, DataSet)

    def serialize(self, obj):
        indices = obj.indices
        size = (len(all_measurements.index) + 7) // 8
        int_repr = int(sum([2 ** int(i) for i in indices]))
        binary = bin(int_repr)
        return int_repr.to_bytes(size, byteorder='big')

    def deserialize(self, str_repr):
        indices = set()
        size = len(str_repr) * 8
        repr = int.from_bytes(str_repr, byteorder='big')
        for i in range(size):
            if 2 ** i & repr:
                indices.add(i)
        return DataSet(indices)


DataSetType = _data_set_type()