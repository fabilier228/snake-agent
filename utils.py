import pickle
from parameters import *


def save_q_table(Q):
    with open(Q_TABLE_FILE, "wb") as f:
        pickle.dump(Q, f)


def update_q_table(state, action, reward, next_state, Q):
    if state not in Q:
        Q[state] = {a: 0 for a in ACTIONS}
    if next_state not in Q:
        Q[next_state] = {a: 0 for a in ACTIONS}
    old_value = Q[state][action]
    next_max = max(Q[next_state].values())
    new_value = (1 - ALPHA) * old_value + ALPHA * (reward + GAMMA * next_max)
    Q[state][action] = new_value


def update_scores_file(path, scores):
    with open(path, 'a+') as f:
        for score in scores:
            f.write(f"{score}\n")


def get_scores(path):
    scores = []
    with open(path, 'r') as f:
        data = f.readlines()
        for i in data:
            scores.append(int(i))

    return scores

