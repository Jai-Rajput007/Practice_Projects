import hashlib
import os

PARTIAL_HASH_BYTES = 1024
CHUNK_SIZE = 4096

def get_file_hash(filepath:str,first_chunk_only:bool=False)->str:
    hash_obj = hashlib.blake2b()
    with open(filepath,'rb') as f:
        if first_chunk_only:
            chunk = f.read(1024)
            hash_obj.update(chunk)
        else:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                hash_obj.update(chunk)
    return hash_obj.hexdigest()
