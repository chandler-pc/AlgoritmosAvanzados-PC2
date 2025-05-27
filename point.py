
POINT_SIZE = 10
POINT_COLOR = (255, 255, 255)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_tuple(self):
        return (self.x, self.y)