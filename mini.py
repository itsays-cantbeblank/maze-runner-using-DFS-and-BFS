import pygame
import random
import time
from collections import deque

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS
WHITE, BLACK, GREEN, BLUE, RED, GRAY = (255, 255, 255), (0, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 0), (200, 200, 200)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver (DFS & BFS)")
clock = pygame.time.Clock()

def generate_maze():
    maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    stack = [(0, 0)]
    visited = set(stack)
    while stack:
        x, y = stack[-1]
        maze[y][x] = 0
        neighbors = [(x + dx, y + dy) for dx, dy in [(0, 2), (2, 0), (-2, 0), (0, -2)]]
        random.shuffle(neighbors)
        for nx, ny in neighbors:
            if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in visited:
                maze[(y + ny) // 2][(x + nx) // 2] = 0
                stack.append((nx, ny))
                visited.add((nx, ny))
                break
        else:
            stack.pop()
    return maze

def draw_maze(maze, path=[]):
    screen.fill(WHITE)
    for y in range(ROWS):
        for x in range(COLS):
            color = BLACK if maze[y][x] == 1 else WHITE
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    for x, y in path:
        pygame.draw.rect(screen, BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, GREEN, (0, 0, CELL_SIZE, CELL_SIZE))  # Start
    pygame.draw.rect(screen, RED, ((COLS - 1) * CELL_SIZE, (ROWS - 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # End
    pygame.display.flip()
    clock.tick(30)

def dfs(maze):
    stack, visited = [(0, 0)], set()
    path = []
    while stack:
        x, y = stack.pop()
        if (x, y) in visited:
            continue
        path.append((x, y))
        visited.add((x, y))
        draw_maze(maze, path)
        time.sleep(0.05)
        if (x, y) == (COLS - 1, ROWS - 1):
            return path
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 0 and (nx, ny) not in visited:
                stack.append((nx, ny))
    return []

def bfs(maze):
    queue, visited = deque([(0, 0)]), set()
    path, parent = [], {}
    while queue:
        x, y = queue.popleft()
        if (x, y) in visited:
            continue
        path.append((x, y))
        visited.add((x, y))
        draw_maze(maze, path)
        time.sleep(0.05)
        if (x, y) == (COLS - 1, ROWS - 1):
            backtrack = (x, y)
            final_path = []
            while backtrack in parent:
                final_path.append(backtrack)
                backtrack = parent[backtrack]
            return final_path[::-1]
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 0 and (nx, ny) not in visited:
                queue.append((nx, ny))
                parent[(nx, ny)] = (x, y)
    return []

def main():
    maze = generate_maze()
    running = True
    while running:
        draw_maze(maze)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    path = dfs(maze)
                    draw_maze(maze, path)
                if event.key == pygame.K_b:
                    path = bfs(maze)
                    draw_maze(maze, path)
    pygame.quit()

if __name__ == "__main__":
    main()
