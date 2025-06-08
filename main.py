import pygame
import random
import pickle
import os
import sys

from utils import save_q_table, update_q_table, update_scores_file
from funcs import get_state, choose_action, move, step
from parameters import *

if os.path.exists(Q_TABLE_FILE):
    with open(Q_TABLE_FILE, "rb") as f:
        Q = pickle.load(f)
else:
    Q = {}


def main():
    scores_over_time = []
    best_score = 0
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = 1
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    score = 0
    episode = 0
    max_episodes = 10000

    running = True
    while running and episode < max_episodes:
        state = get_state(snake, food, direction)
        action = choose_action(state, Q)
        direction = move(direction, action)
        new_head = step(snake, direction)

        reward = 0
        done = False
        if (
                new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
                new_head in snake
        ):
            reward = -10
            done = True
        else:
            snake.insert(0, new_head)
            if new_head == food:
                reward = 20
                score += 1
                while True:
                    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                    if food not in snake:
                        break
            else:
                snake.pop()
                reward = -0.1

        next_state = get_state(snake, food, direction)
        update_q_table(state, action, reward, next_state, Q)

        screen.fill(BLACK)
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        font = pygame.font.SysFont(None, 24)
        img = font.render(f"Score: {score}  Episode: {episode}  Best: {best_score}", True, WHITE)
        screen.blit(img, (10, 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        if done:
            scores_over_time.append(score)
            if score > best_score:
                best_score = score
            episode += 1

            snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
            direction = 1
            score = 0

            if episode % 100 == 0:
                print(f"Episode {episode}: saving Q-table...")
                save_q_table(Q)

        clock.tick(0)

    save_q_table(Q)
    update_scores_file(SCORES_FILE, scores_over_time)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
