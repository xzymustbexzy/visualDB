import os
from collections import OrderedDict

import numpy as np

from descriptor_lib.descriptor import Descriptor
import config


class DescriptorGroup(object):

    def __init__(self, 
            filepath,
            feature_size,
            metric,
            dtype=None,
            itemsize=None,
            ):
        """Maintain a list of descriptions.
        
        Args:
            filepath: str, filepath to store feature descriptor group.
            feature_size: int, fix length of feature vector.
            dtype: numpy.dtype, type of feature vector.
            metric: str, measures of distance between feature vectors.
        """
        # Keyed by description id.
        self.description_table = OrderedDict()
        self.filepath = filepath
        self.feature_size = feature_size
        self.metric = metric
        self._dtype = dtype
        self._itemsize = itemsize

    def _get_numpy_vector_info(self, attibute_name, numpy_attr):
        """Get attribute (like dtpye, itemsize and so on) from the first vector.
        If description group is empty, return None.
        
        Args:
            attibute_name: str, internal attribute name.
            numpy_attr: str, numpy array's attribute name.
        """
        if getattr(self, attibute_name) is not None:
            return getattr(self, attibute_name)
        if len(self.description_table) == 0:
            return None
        elem = next(self.description_table.values())
        np_attr = getattr(elem.feature_vec, numpy_attr)
        setattr(self, attibute_name, np_attr)
        return np_attr

    @property
    def dtype(self):
        return self._get_numpy_vector_info('_dtype', 'dtype')
        
    @property
    def itemsize(self):
        return self._get_numpy_vector_info('_itemsize', 'itemsize')

    def add(self, descriptor: Descriptor):
        """Add a descriptor into group. If descriptor id is exist,
        it will be updated. 
        
        Args:
            descriptor: Descriptor, descriptor to be added.
        """
        self.description_table[descriptor.id] = descriptor

    def get(self, id):
        """Retrieve corresponding descriptor from description group.

        Args:
            id: object, id of descriptor.
        
        Returns:
            Descriptor: the retrieved descriptor.

        Raise:
            KeyError: raise if descriptor of ``id`` not found.
        """
        return self.description_table[id]

    def delete(self, id):
        """Delete descriptor from description group.
        
        Args:
            id: object, id of descriptor.

        Returns:
            bool: ``True`` if delete successfully.
        """
        if id in self.description_table:
            del self.description_table[id]
            return True
        return False


    def _numpy_vector_to_binary(self, feature):
        """Convert one-dimension numpy array to bytes array."""
        return feature.tobytes(order='C')

    def flush(self):
        """Write descripton group to file system.

        Args:
            filepath: str, filepath to store descriptors.

        Returns:
            bool: return `True` if write successfully.
        """
        path = os.path.join(config.db_root, self.filepath)
        with open(path, 'wb') as f:
            for desc in self.description_table.values():
                f.write(self._numpy_vector_to_binary(desc.feature_vec))

    def load(self):
        """Load descriptor' feature from file"""
        if self.itemsize is None or self.dtype is None:
            raise NotImplementedError('metadata not loaded!')
        path = os.path.join(config.db_root, self.filepath)
        with open(path, 'rb') as f:
            data = f.read()
        data_len = len(data)
        itemsize = self.itemsize
        i = 0
        it = iter(self.description_table)
        while i < data_len:
            desc = next(it)
            desc.feature_vec = np.frombuffer(
                        data[i: i+itemsize], 
                        dtype=self.dtype)
            i += itemsize
