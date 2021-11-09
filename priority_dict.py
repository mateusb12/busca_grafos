class PriorityList:
    def __init__(self):
        self.table = []

    def add(self, label: int, priority):
        self.table.append([label, priority])
        # Reorder the table according to priority
        self.table = sorted(self.table, key=lambda x: x[1])

    def get_first_item(self):
        return self.table[0]

    def pop(self, index: int = None):
        if index is None:
            return self.table.pop()
        else:
            return self.table.pop(index)

    def __getitem__(self, item):
        return self.table[item]

    def __len__(self):
        return len(self.table)

    def __iter__(self):
        return iter(self.table)

    def __str__(self):
        return str(self.table)

    def __repr__(self):
        return str(self.table)

    def __contains__(self, item):
        return item in self.table

    def __delitem__(self, item):
        del self.table[item]

    def __setitem__(self, key, value):
        self.table[key] = value


test1 = PriorityList()
test1.add(5, 7)
test1.add(10, 2)
test1.add(4, 5)
print(test1[2])