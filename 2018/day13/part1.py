import numpy as np
import pdb
import time
import array2gif as gif
import scipy.misc as misc
import random

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

frames = []

def print_state(inp, carts, col_dict, frames):
    # reset = '\u001b[0m' 
    height = len(inp)
    width = len(inp[0])
    image = np.zeros((height, width, 3))

    carts_d = set()
    for cart in carts:
        x, y = cart.pos
        image[y, x] = cart.color
        carts_d.add((x, y))
        col_dict[x, y] = cart.color

    for y in range(len(inp)):
        for x in range(len(inp[y])):
            if (x, y) not in carts_d:
                if (x, y) in col_dict:
                    color = col_dict[(x, y)]
                    image[y, x, :] = color

    frames.append(misc.imresize(image, (height*2, width*2),
                                interp='nearest'))


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

def generate_color():
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
           )

inp = read_input("input.txt", str)

carts = []

for y in range(len(inp)):
    line = inp[y]
    for x in range(len(line)):
        c = line[x]
        if c == '<':
            cart = Cart((x, y), LEFT, generate_color())
            carts.append(cart)
        elif c == '>':
            cart = Cart((x, y), RIGHT, generate_color())
            carts.append(cart)
        elif c == 'v':
            cart = Cart((x, y), DOWN, generate_color())
            carts.append(cart)
        elif c == '^':
            cart = Cart((x, y), UP, generate_color())
            carts.append(cart)
    inp[y] = line.replace('>','-').replace('<','-').replace('v','|').replace('^','|')

max_it = 1000
it = 0
while it < max_it:
    print_state(inp, carts, col_dict, frames)
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
    it += 1

    #time.sleep(0.02)

gif.write_gif(frames, 'test.gif', fps=20)

