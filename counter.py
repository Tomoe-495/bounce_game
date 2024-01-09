

class Counter:
    count = 0

    def counting(self):
        self.count += 1
        if self.count > 120:
            self.count = 0



count = Counter()
