

class Counter:
    count = 0

    def counting(self):
        self.count += 1
        if self.count > 600:
            self.count = 0



count = Counter()
