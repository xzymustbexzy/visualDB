import os

import faiss
import numpy as np

from descriptor_lib.descriptor_group import DescriptorGroup
import config


class FaissEngine(object):

    def __init__(self,
            descriptor_group,
            filename):
        """Descriptor indexing and storage engine powered by Faiss.
        
        Args:
            descriptor_group: DescriptorGroup, the descriptor_group 
                to be indexing or to be stored.
            filename: str, filename for store index file.
            
        """
        self.descriptor_group = descriptor_group
        self.X = None
        self.index = None
        self.filename = filename


    def _get_X(self):
        """Convert feature of descriptor_group to matrix."""
        if self.X is None:
            dg = self.descriptor_group
            self.X = np.zeros(
                    len(dg), dg.feature_size, 
                    dtype=dg.dtype)
            for i, desc in enumerate(dg.description_table.values()):
                self.X[i, :] = desc.feature_vec
        return self.X

    def get_index(self):
        """Get index of """
        if self.index is None:
            self.index = faiss.IndexFlatL2(self._get_X())
        return self.index
    
    def save_index(self):
        """Save the index file."""
        index = self.get_index()
        path = os.path.join(config.db_feature_index_path, self.filename)
        faiss.write_index(index, path)

    def load_index(self):
        """Load index from file."""
        path = os.path.join(config.db_feature_index_path, self.filename)
        self.index = faiss.read_index(path)

    def k_similar_samples(self, query, k=1):
        """Query the most similar k samples."""
        index = self.get_index()
        D, I = index.search(query, k)
        return D, I

