import numpy as np
import pdb
import time

TURN_LEFT = 0
TURN_STRAIGHT = 1
TURN_RIGHT = 2

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

NORMAL = 0
INTERSECTION = 1

def read_input(fname, data_type):
    nums = []
    with open(fname) as f:
        nums = [data_type(x) for x in f.readlines()]
    return nums 

class Cart:

    def __init__(self, pos, orientation, color):
        self.pos = pos
        self.next_turn = 0
        self.orientation = orientation
        self.color = color

    def turn(self):
        t = self.next_turn
        self.next_turn = (self.next_turn + 1) % 3
        if t == TURN_LEFT:
            self.orientation = (self.orientation + 1) % 4
        elif t == TURN_RIGHT:
            self.orientation = (self.orientation - 1) % 4

    def inc(self, dxdy):
        dx, dy = dxdy
        x, y = self.pos
        self.pos = (x + dx, y + dy)


col_dict = {}

def find_cart_at(pos, carts):
    for cart in carts:
        if cart.pos == pos:
            return cart
    return None

def print_state(inp, carts, col_dict):
    reset = '\u001b[0m' 
    carts_d = {}
    for cart in carts:
        x, y = cart.pos
        c = ''
        if cart.orientation == LEFT:
            c = '<'
        elif cart.orientation == RIGHT:
            c = '>'
        elif cart.orientation == UP:
            c = '^'
        elif cart.orientation == DOWN:
            c = 'v'
        carts_d[(x, y)] = cart.color + c + reset

    lines = []
    for y in range(len(inp)):
        row = []
        for x in range(len(inp[y])):
            if (x, y) in carts_d:
                row.append(carts_d[(x, y)])
                cart = find_cart_at((x, y), carts)
                col_dict[(x, y)] = cart.color
            else:
                if (x, y) in col_dict:
                    color = col_dict[(x, y)]
                    row.append(color + inp[y][x] + reset)
                else:
                    row.append(inp[y][x])

        lines.append(''.join(row))
    print(''.join(lines))


def get_collision(carts):
    seen = set()
    for cart in carts:
        if cart.pos in seen:
            return cart.pos
        else:
            seen.add(cart.pos)
    return None


def remove_carts_at(carts, pos):
    edited = True
    while edited:
        edited = False
        for i in range(len(carts)):
            if carts[i].pos == pos:
                carts.remove(carts[i])
                edited = True
                break

inp = read_input("input.txt", str)

carts = []

for y in range(len(inp)):
    line = inp[y]
    colors = ['\u001b[31m', '\u001b[32m', 
              '\u001b[33m', '\u001b[34m', '\u001b[35m']
    color_i = 0
    for x in range(len(line)):
        c = line[x]
        if c == '<':
            cart = Cart((x, y), LEFT, colors[color_i])
            carts.append(cart)
        elif c == '>':
            cart = Cart((x, y), RIGHT, colors[color_i])
            carts.append(cart)
        elif c == 'v':
            cart = Cart((x, y), DOWN, colors[color_i])
            carts.append(cart)
        elif c == '^':
            cart = Cart((x, y), UP, colors[color_i])
            carts.append(cart)
        color_i = (color_i + 1) % len(colors)
    inp[y] = line.replace('>','-').replace('<','-').replace('v','|').replace('^','|')

while True:
    print_state(inp, carts, col_dict)
    collided = []
    col_set = set()
    for cart in carts:
        if cart.pos in col_set:
            continue

        x, y = cart.pos

        new_pos = None
        if cart.orientation == LEFT:
            new_pos = (x-1, y)
        elif cart.orientation == RIGHT:
            new_pos = (x+1, y)
        elif cart.orientation == UP:
            new_pos = (x, y-1)
        elif cart.orientation == DOWN:
            new_pos = (x, y+1)

        nx, ny = new_pos
        collision_occurred = False
        for c2 in carts:
            if c2.pos == (nx, ny):
                collided.append((c2, cart, (nx, ny)))
                col_set.add((nx, ny))
                collision_occurred = True

        if not collision_occurred:
            track_piece = inp[ny][nx]
            if track_piece == '\\':
                if cart.orientation == DOWN:
                    cart.orientation = RIGHT 
                elif cart.orientation == UP:
                    cart.orientation = LEFT
                elif cart.orientation == RIGHT:
                    cart.orientation = DOWN
                else:
                    cart.orientation = UP
            elif track_piece == '/':
                if cart.orientation == DOWN:
                    cart.orientation = LEFT 
                elif cart.orientation == UP:
                    cart.orientation = RIGHT 
                elif cart.orientation == RIGHT:
                    cart.orientation = UP 
                else:
                    cart.orientation = DOWN
            elif track_piece == '+':
                cart.turn()

            cart.pos = new_pos

    for c1, c2, pos in collided:
        if c1 in carts:
            carts.remove(c1)
        if c2 in carts:
            carts.remove(c2)
        # print("COLLISION AT", (nx, ny))
    if len(carts) == 1:
        print("ONLY CART LEFT AT", carts[0].pos)
        break

    time.sleep(0.02)


