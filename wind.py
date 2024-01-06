import random


class Wind:
    pressure = 0.5
    speed = pressure
    acc = 0.001

    def update(self):
        rand = random.randint(0, 500)
        if rand ==  5:
            self.speed = random.uniform(0.1, 1.0)

        if self.pressure < self.speed:
            # self.pressure += self.acc
            self.pressure = min(self.speed, self.pressure + self.acc)
        elif self.pressure > self.speed:
            self.pressure = max(self.speed, self.pressure - self.acc)

