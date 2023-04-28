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
