# class SpaceSaving():
#     def __init__(self, len):
#         # element, count, epsilon
#         self.list = list(map(lambda _: [None, 0, 0], range(0, len)))
#         self.len = len
#         self.hash = hash

#     def add(self, value):
#         position = self.hash(value) % self.len
#         if self.list[position][0] == value:
#             self.list[position][1] += 1
#         else:
#             min_index = 0
#             min = float('inf')
#             for i in range(0, self.len):
#                 if self.list[i][1] < min:
#                     min = self.list[i][1]
#                     min_index = i

#             self.list[min_index][0] = value
#             self.list[min_index][1] += 1
#             self.list[min_index][2] = int(min)

#     def query(self, n, support):
#         def sort_fn(e1):
#             return -e1[1]

#         clone = list(self.list[0:])
#         clone.sort(key=sort_fn)

#         sorted_list = list(clone[0:n])

#         guaranteed = True
#         for i in range(0, n):
#             if sorted_list[i][1] - sorted_list[i][2] < support:
#                 guaranteed = False

#         return (sorted_list, guaranteed)


class SpaceSavingEntry():
    def __init__(self, count=1, error=0):
        self.count = count
        self.error = error

    def __str__(self):
        return f"SpaceSavingEntry(count={self.count}, error={self.error})"


class SpaceSaving():
    def __init__(self, dim):
        self.dim = dim
        self.hash_table = dict()

    def add(self, value):
        if value in self.hash_table:
            self.hash_table[value].count += 1
        else:

            if len(self.hash_table) >= self.dim:

                min_item, min_spacesaving_entry = min(self.hash_table.items(),
                                                      key=lambda e: e[1].count)
                del self.hash_table[min_item]
                self.hash_table[value] = SpaceSavingEntry(
                    min_spacesaving_entry.count + 1,
                    min_spacesaving_entry.count)

            else:
                self.hash_table[value] = SpaceSavingEntry()

    def query(self, n):
        return list(
            map(
                lambda e: [e[0], str(e[1])],
                sorted(self.hash_table.items(),
                       key=lambda e: -e[1].count)[0:n]))
