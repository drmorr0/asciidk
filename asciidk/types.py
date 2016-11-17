
class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, p2):
        return Point(self.x + p2.x, self.y + p2.y)

    def __sub__(self, p2):
        return Point(self.x - p2.x, self.y - p2.y)

    def __str__(self):
        return "({x}, {y})".format(x=self.x, y=self.y)

    def __eq__(self, p2):
        return self.x == p2.x and self.y == p2.y

    def __hash__(self):
        return hash((self.x, self.y))


class Grid:
    def __init__(self, width, height, dungeon):
        from asciidk.obj.rock import Rock
        self.grid = [[[Rock(Point(x, y), dungeon)] for x in range(width)] for y in range(height)] 

    def top_obj(self, pos):
        if self.grid[pos.y][pos.x]:
            return self.grid[pos.y][pos.x][-1]
        return None

    def add_obj(self, obj):
        self.grid[obj.pos.y][obj.pos.x].append(obj)

    def rem_obj(self, obj):
        self.grid[obj.pos.y][obj.pos.x].remove(obj)

    def pop_obj(self, pos):
        if self.grid[pos.y][pos.x]:
            return self.grid[pos.y][pos.x].pop()
        return None

    def stack(self, pos):
        return self.grid[pos.y][pos.x]

    def set_stack(self, pos, stack):
        self.grid[pos.y][pos.x] = stack

