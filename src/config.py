import os

# Root path for physical storage.
db_root = '../db'

# Path for feature of descriptor group storage.
db_descriptor_path = os.path.join(db_root, 'descriptor_group')

# Path for feature index.
db_feature_index_path = os.path.join(db_root, 'feature_index')

# Standard loopback interface address (localhost)
HOST = "127.0.0.1" 

# Port to listen on (non-privileged ports are > 1023)
PORT = 33333  

