import random

_memomask = {}

def hash_n(n):
    mask = _memomask.get(n)
    if mask is None:
        random.seed(n)
        mask = _memomask[n] = random.getrandbits(32)

    def myhash(x):
        return hash(x) ^ mask
    return myhash

# The built-in hash is decent and pretty efficient -- xor'ing it with a number depending (but in a sufficiently chaotic way) from the index within the family just seems another decent/efficient way to turn that one hash function into a family.
