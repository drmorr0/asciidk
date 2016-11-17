
from asciidk.constants import UP
from asciidk.constants import DOWN
from asciidk.constants import RIGHT
from asciidk.constants import LEFT
from asciidk.types import Point
from asciidk.util import move_pos
from asciidk.util import rotate_right
from asciidk.util import sign

def _get_steps(target_pos, parent):
    steps = []

    current_pos = target_pos
    while parent[current_pos]:
        steps.append(parent[current_pos]['dir'])
        current_pos = parent[current_pos]['pos']

    steps.reverse()
    return steps

def compute_path_to_target(start_pos, target_pos, dungeon):
    parent = {start_pos: None}
    queue = [start_pos]

    while queue:
        current_pos = queue.pop(0)

        if current_pos == target_pos:
            return _get_steps(target_pos, parent)

        if not dungeon.is_passable(current_pos) and not dungeon.has_mob_or_player(current_pos):
            continue

        delta_x = current_pos.x - target_pos.x
        delta_y = current_pos.y - target_pos.y

        if delta_y == 0:
            direction = RIGHT if sign(delta_x) < 0 else LEFT
        else:
            direction = DOWN if sign(delta_y) < 0 else UP

        for i in range(4):
            direction = rotate_right(direction, i)
            next_pos = move_pos(current_pos, direction)
            if next_pos not in parent:
                parent[next_pos] = {'pos': current_pos, 'dir': direction}
                queue.append(next_pos)

    raise Exception("ERROR: no path to target found")
