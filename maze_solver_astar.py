# --- Sadulla Abdukodirov, 221ADB187 ---

import heapq
import sys
from typing import List, Tuple, Dict

# --- Node class used for priority queue in A* search ---
# Keeps track of current position, distance from start, total coins collected, and path taken
class Node:
    def __init__(self, x: int, y: int, dist: int, coins: int, path: List[Tuple[int, int]]):
        self.x = x
        self.y = y
        self.dist = dist  # number of steps taken so far
        self.coins = coins  # total coins collected so far
        self.path = path  # list of coordinates from start to current

    def __lt__(self, other):
        # This ensures the priority queue favors shorter paths,
        # and among them, the ones with fewer coins collected
        return (self.dist, self.coins) < (other.dist, other.coins)

# --- Direction vectors for 8-way movement ---
# Includes horizontal, vertical, and diagonal directions
DIRECTIONS = [
    (-1, 0), (1, 0), (0, -1), (0, 1),       # up, down, left, right
    (-1, -1), (-1, 1), (1, -1), (1, 1)      # diagonals
]

# --- Function to read and parse maze from file ---
def load_maze(filepath: str) -> Tuple[List[List[str]], Tuple[int, int], Tuple[int, int]]:
    maze = []
    start = goal = (-1, -1)
    with open(filepath, 'r') as f:
        for i, line in enumerate(f):
            row = list(line.strip())
            for j, cell in enumerate(row):
                if cell == 'S':
                    start = (i, j)
                elif cell == 'G':
                    goal = (i, j)
            maze.append(row)
    return maze, start, goal

# --- A* search algorithm implementation ---
# This version finds the shortest path from S to G
# Among all shortest paths, it chooses the one with the minimum coins collected
# Allows diagonal movement

def solve_maze(maze: List[List[str]], start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[int, List[Tuple[int, int]]]:
    rows, cols = len(maze), len(maze[0])
    visited: Dict[Tuple[int, int], Tuple[int, int]] = {}  # maps coordinates to (distance, coin count)
    
    # Priority queue for A* search
    pq = []
    heapq.heappush(pq, Node(start[0], start[1], 0, 0, [start]))

    while pq:
        current = heapq.heappop(pq)
        pos = (current.x, current.y)

        # Check if we've reached the goal
        if pos == goal:
            return current.coins, current.path

        # Skip processing if we've already visited with a better or equal state
        if pos in visited and visited[pos] <= (current.dist, current.coins):
            continue

        visited[pos] = (current.dist, current.coins)

        # Explore all 8 possible directions
        for dx, dy in DIRECTIONS:
            nx, ny = current.x + dx, current.y + dy

            # Check bounds and wall collisions
            if 0 <= nx < rows and 0 <= ny < cols:
                cell = maze[nx][ny]
                if cell == 'X':  # wall
                    continue
                # Convert cell to coin value if numeric
                coins = 0 if cell in {'S', 'G'} else int(cell)
                heapq.heappush(pq, Node(nx, ny, current.dist + 1, current.coins + coins, current.path + [(nx, ny)]))

    return -1, []  # No path found

# --- Main function to run solver for all provided maze files ---
def run_all():
    # List of maze files and labels
    mazes = [
        ("maze_11x11.txt", "maze_11x11"),
        ("maze_31x31.txt", "maze_31x31"),
        ("maze_101x101.txt", "maze_101x101")
    ]

    results = []
    for filepath, label in mazes:
        maze, start, goal = load_maze(filepath)
        coins, path = solve_maze(maze, start, goal)
        print(f"{label} -> Coins Collected: {coins}, Steps: {len(path)}")
        results.append(str(coins))

    # Output format for submission
    print("\nSubmission Format:")
    print(",".join(results))
    print("Time Complexity: O(N^2 log N) due to priority queue and revisits")
    print("Space Complexity: O(N^2) for visited map and path tracking")

# --- Program entry point ---
if __name__ == "__main__":
    run_all()
