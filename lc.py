from bitarray import bitarray
from hash_family import hash_n
import math


class LinearCounter():

    def __init__(self, len, hash_fn=0):
        self.hash = hash_n(hash_fn)
        self.bit_map = bitarray(len)
        self.bit_map.setall(False)

    def add(self, value):
        self.bit_map[self.hash(value) % len(self.bit_map)] = True

    def count(self):
        return self.bit_map.count(True)

    def count_estimation(self):
        """
        Gets the current value of the bitmap, to do that we follow the formula:
        -size * ln(unset_bits/size)
        """
        ratio = float(self.bit_map.count(False)) / float(len(self.bit_map))
        if ratio <= 0.0:
            return len(self.bit_map)
        else:
            return int(-len(self.bit_map) * math.log(ratio))

    def contains(self, value):
        # if it returns False the value isn't into the lc
        return True if self.bit_map[self.hash(value) % len(self.bit_map)] else False

    def intersect(self, that):
        to_ret = LinearCounter(len(self.bit_map))
        for i in range(0, len(self.bit_map)):
            to_ret.bit_map[i] = self.bit_map[i] and that.bit_map[i]
        return to_ret
