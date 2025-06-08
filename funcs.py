import random
import numpy as np

from parameters import *


def get_state(snake, food, direction):
    head = snake[0]
    dx = np.sign(food[0] - head[0])
    dy = np.sign(food[1] - head[1])
    return (dx, dy, direction)


def choose_action(state, Q):
    if state not in Q:
        Q[state] = {a: 0 for a in ACTIONS}
    if random.random() < EPSILON:
        return random.choice(ACTIONS)
    else:
        max_q = max(Q[state].values())
        best_actions = [a for a, q in Q[state].items() if q == max_q]
        return random.choice(best_actions)


def move(direction, action):
    if action == 1:
        direction = (direction - 1) % 4
    elif action == 2:
        direction = (direction + 1) % 4
    return direction


def step(snake, direction):
    head = snake[0]
    if direction == 0:
        new_head = (head[0], head[1] - 1)
    elif direction == 1:
        new_head = (head[0] + 1, head[1])
    elif direction == 2:
        new_head = (head[0], head[1] + 1)
    else:
        new_head = (head[0] - 1, head[1])
    return new_head
