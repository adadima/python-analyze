class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dist = self.distance()

    def distance(self):
        return (self.x**2 + self.y**2)**0.5