from bitarray import bitarray
from hash_family import hash_n
import math


class BloomFilter():

    def __init__(self, len, n_hash_fn=1):
        self.hashes = [hash_n(i) for i in range(n_hash_fn)]
        self.bit_map = bitarray(len)
        self.bit_map.setall(False)

    def add(self, value):
        for hash in self.hashes:
            self.bit_map[hash(value) % len(self.bit_map)] = True

    def count(self):
        return self.bit_map.count(True)

    def count_estimation(self):
        """
        Gets the current value of the bitmap, to do that we follow the formula:
        -size * ln(unset_bits/size)
        """
        ratio = 1 - float(self.bit_map.count(True)) / float(len(self.bit_map))
        return int(-(len(self.bit_map) / len(self.hashes)) * math.log(ratio))
        # ratio = float(self.bit_map.count(False)) / float(len(self.bit_map))
        # if ratio <= 0.0:
        #     return len(self.bit_map)
        # else:
        #     print(len(self.hashes))
        #     return int(-len(self.bit_map) * math.log(ratio) / len(self.hashes))

    def contains(self, value):
        # if it returns False the value isn't into the lc
        for hash in self.hashes:
            if self.bit_map[hash(value) % len(self.bit_map)] == 0:
                return False
        return True

    def intersect(self, that):
        to_ret = BloomFilter(len(self.bit_map), len(self.hashes))
        for i in range(0, len(self.bit_map)):
            to_ret.bit_map[i] = self.bit_map[i] and that.bit_map[i]
        return to_ret

    def union(self, that):
        to_ret = BloomFilter(len(self.bit_map), len(self.hashes))
        for i in range(0, len(self.bit_map)):
            to_ret.bit_map[i] = self.bit_map[i] or that.bit_map[i]
        return to_ret
