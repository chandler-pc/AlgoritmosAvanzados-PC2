class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_tuple(self):
        return (self.x, self.y)
    
    @staticmethod
    def cross(a, b, c):
        return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)
    
    @staticmethod
    def distance(a, b):
        return ((b.x - a.x) ** 2 + (b.y - a.y) ** 2) ** 0.5

    def __str__(self):
        return f"Point({self.x}, {self.y})"