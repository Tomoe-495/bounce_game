import random


class Wind:
    pressure = 0.5

    def update(self):
        rand = random.randint(0, 500)
        if rand ==  5:
            self.pressure = random.uniform(0.1, 1.0)

