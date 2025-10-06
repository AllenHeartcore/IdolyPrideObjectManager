"""
utils.py
General-purpose utilities: hashing, decorators, etc.
"""

from cryptography.hazmat.primitives import hashes


def md5sum(data: bytes) -> bytes:
    """Calculates MD5 hash of the given data."""
    digest = hashes.Hash(hashes.MD5())
    digest.update(data)
    return digest.finalize()
