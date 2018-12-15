import numpy as np
from readinput import read_input

inp = [l.replace('\n', '') for l in read_input("input.txt", str)]

def print_state(units, walls):
    w, h = walls.shape
    lines = []
    for y in range(h):
        row = []
        for x in range(w):
            if (x, y) not in units:
                row.append('#' if walls[x, y] else '.')
            else:
                row.append(units[x, y][1])
        lines.append("".join(row))
    print("\n".join(lines))


def print_state2(units, walls, steps):
    w, h = walls.shape
    lines = []
    for y in range(h):
        row = []
        for x in range(w):
            if (x, y) in steps:
                row.append('X')
            elif (x, y) not in units:
                row.append('#' if walls[x, y] else '.')
            else:
                row.append(units[x, y][1])
        lines.append("".join(row))
    print("\n".join(lines))


def is_over(units):
    seen_g = False
    seen_e = False
    for _, t, _, _ in units.values():
        if t == 'E':
            if seen_g:
                return False
            else:
                seen_e = True
        elif t == 'G':
            if seen_e:
                return False
            else:
                seen_g = True
    return True


def targets_in_range(units, x, y, t):
    targs = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if abs(i) != abs(j):
                if (x+i,y+j) in units and t != units[x+i,y+j][1]:
                    targs.append((x+i, y+j))
    return sorted(targs, key=tup_key)


def steps_in_range(units, walls, x, y):
    steps = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if abs(i) != abs(j):
                nx = x + i
                ny = y + j
                if not walls[nx, ny] and (nx, ny) not in units:
                    steps.append((nx, ny))
    return sorted(steps, key=tup_key)


def steps_in_range2(units, walls, x, y, thisid):
    steps = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if abs(i) != abs(j):
                nx = x + i
                ny = y + j
                if not walls[nx, ny] and \
                   ((nx, ny) not in units or units[nx, ny][0] == thisid):
                    steps.append((nx, ny))
    return sorted(steps, key=tup_key)


def distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)


def is_reachable(walls, units, p1, p2, visited, forbidden=None):
    return breadth_first_search(walls, units, p1, p2) is not None


def shortest_path(walls, units, p1, p2):
    def obstructed(x, y):
        w, h = walls.shape
        if p1 == (x, y) or p2 == (x, y):
            return False
        return x >= w or y >= h or walls[x, y] \
                    or (x, y) in units
    path = pathfinding.find_path(p1, p2, obstructed)
    return len(path) 


def breadth_first_search(walls, units, p1, p2):
    id = -1
    if p2 in units:
        id, _, _, _ = units[p2]

    open_set = []

    closed_set = set()

    meta = {}

    root = p1
    meta[root] = None
    open_set.append(root)

    while open_set:

        subtree_root = open_set.pop(0)
        
        if p2 == subtree_root:
            return len(construct_path(subtree_root, meta))

        steps = steps_in_range2(units, walls, *subtree_root, id)
        for child in steps:
            
            if child in closed_set:
                continue
            
            if child not in open_set:
                meta[child] = subtree_root
                open_set.append(child)
        
        closed_set.add(subtree_root)
    return None


def construct_path(state, meta):
    action_list = list()
  
    while meta[state] is not None:
      state = meta[state]
      action_list.append(state)
    
    return action_list


def get_reachable_targets(units, walls, pos):
    x, y = pos
    res = []
    for (tx, ty) in units:
        if (tx, ty) != pos:
            _, etyp, _, _ = units[(tx, ty)]
            _, ttyp, _, _ = units[(x, y)]
            if ttyp != etyp and \
               is_reachable(walls, units, (x, y), (tx, ty), set()):
                res.append((tx, ty))
    return sorted(res, key=tup_key)


def tup_key(tup):
    x, y = tup
    return (y, x)


attack_power = 15

while True:
    attack_power += 1

    print()
    print("Trying AP", attack_power)
    print()

    # (x, y) -> (id, type, AP, HP)
    units = {}
    # id -> ((x, y), type)
    ids = {}

    height = len(inp)
    width = len(inp[0])

    walls = np.zeros((width, height), dtype='uint8')

    curr_id = 0
    for y in range(height):
        for x in range(width):
            c = inp[y][x]
            walls[x, y] = c == '#'
            if c in 'EG':
                pos = (x, y)
                typ = c
                id = curr_id
                units[pos] = (id, typ, 
                              3 if typ == 'G' else attack_power, 200)
                ids[id] = (pos, typ)
                curr_id += 1
    it = 0
    elf_died = False
    while not is_over(units) and not elf_died:
        print()
        print("Round", it)
        it += 1
        print_state(units, walls)
        print(units)
        positions = sorted(list(units.keys()), key=tup_key)
        for x, y in positions:

            if (x, y) not in units:
                continue

            id, typ, ap, hp = units[x, y]
            targets = targets_in_range(units, x, y, typ)

            new_x = x
            new_y = y
            
            # no target, move
            if not targets:
                steps = []
                for tx, ty in get_reachable_targets(units, walls, (x, y)):
                    tid, ttype, tap, thp = units[tx, ty]
                    steps.extend(steps_in_range(units, walls, tx, ty))

                # if it can't find a path to an enemy, end the turn

                if not steps:
                    continue


                steps = list(filter(lambda pos: is_reachable(walls, units, (x, y), pos, set()), steps))

                paths = [(breadth_first_search(walls, units, (px, py), (x, y)), py, px)
                        for (px, py) in steps]
                _, sy, sx = min(
                    paths
                    )

                # find the step that is to be moved
                step_candidates = steps_in_range(units, walls, x, y)
                step_candidates = list(filter(lambda pos: is_reachable(walls, units, (sx, sy), pos, set()), step_candidates))

                _, new_y, new_x = min(
                    [(breadth_first_search(walls, units, (px, py), (sx, sy)), py, px)
                        for (px, py) in step_candidates])

            targets = targets_in_range(units, x, y, typ)
            
            # update position
            if new_x != x or new_y != y:
                u = units[x, y]
                del units[x, y]
                units[new_x, new_y] = u
                id = u[0]
                _, typ = ids[id]
                ids[id] = ((new_x, new_y), typ)
                
            
            x = new_x
            y = new_y
            targets = targets_in_range(units, x, y, typ)
            if targets:
                points, ty, tx = min(
                    [(units[px, py][3], py, px) for px, py in targets]
                )
                points -= ap
                
                # enemy died
                if points <= 0:
                    print("UNIT", units[tx, ty], "died")
                    id, typ, _, _ = units[tx, ty]
                    if typ == 'E':
                        print()
                        print("ELF DIED")
                        print()
                        elf_died = True
                        break
                    del units[tx, ty]
                    del ids[id]
                else:
                    # update HP
                    id, typ, ap, hp = units[tx, ty]
                    units[(tx, ty)] = (id, typ, ap, points)

    hps = sum(unit[3] for unit in units.values())

    print("Outcome:", it*hps, "Maybe:", (it-1)*hps, "It:", it, "Hps:", hps)
    if not elf_died:
        break

