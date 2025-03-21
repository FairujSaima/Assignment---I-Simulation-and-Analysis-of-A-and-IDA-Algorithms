import pygame
from queue import PriorityQueue
import random

class Agent(pygame.sprite.Sprite):
    def __init__(self, environment, grid_size):
        super().__init__()
        self.image = pygame.Surface((grid_size, grid_size))
        self.image.fill((0, 0, 255))  
        self.rect = self.image.get_rect()
        self.grid_size = grid_size
        self.environment = environment
        self.position = [0, 0]  
        self.task_completed = 0
        self.completed_tasks = []
        self.path = []  
        self.moving = False  
        self.total_path_cost = 0  
    def move(self):
        """Move the agent along the path."""
        if self.path:
            next_position = self.path.pop(0)  
            self.position = list(next_position)  
            self.rect.topleft = (self.position[0] * self.grid_size, self.position[1] * self.grid_size)
            
            self.total_path_cost += 1  
            self.check_task_completion()  
        else:
            self.moving = False  

    def calculate_path_cost(self):
        """Calculate path cost based on the number of moves made."""
        
        return len(self.path) if self.path else 0
        
    def check_task_completion(self):
        """Check if a task is completed and find the next task."""
        position_tuple = tuple(self.position)
        if position_tuple in self.environment.task_locations:
            task_number = self.environment.task_locations.pop(position_tuple)
            self.task_completed += 1
            self.completed_tasks.append(task_number)
           
            self.total_path_cost += self.calculate_path_cost()
            
            if self.environment.task_locations:  
                self.find_nearest_task()
            else:
                self.moving = False  

    def find_nearest_task(self):
        """Find the nearest task using A*."""
        nearest_task = None
        shortest_path = None
        min_path_cost = float('inf')  

        for task_position in self.environment.task_locations.keys():
            path, path_cost = self.find_path_to(task_position)
            if path:
                if path_cost < min_path_cost:
                    min_path_cost = path_cost
                    shortest_path = path
                    nearest_task = task_position
            else:
                print(f"WARNING: No path found to task at {task_position}")

        if shortest_path:
            self.path = shortest_path[1:]  
            self.moving = True

    def find_path_to(self, target):
        """A* pathfinding algorithm."""
        start = tuple(self.position)
        goal = target
        open_set = PriorityQueue()
        open_set.put((0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while not open_set.empty():
            current = open_set.get()[1]

            if current == goal:
                path, cost = self.reconstruct_path(came_from, current, g_score)
                return path, cost

            neighbors = self.get_neighbors(*current)
            for neighbor in neighbors:
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    if neighbor not in [i[1] for i in open_set.queue]:
                        open_set.put((f_score[neighbor], neighbor))

        return None  

    def heuristic(self, position, goal):
        """Manhattan distance heuristic."""
        return abs(position[0] - goal[0]) + abs(position[1] - goal[1])

    def reconstruct_path(self, came_from, current, g_score):
        """Reconstruct path from A*."""
        total_path = [current]
        total_cost = g_score[current]

        while current in came_from:
            current = came_from[current]
            total_path.append(current)

        total_path.reverse()
        return total_path, total_cost

    def get_neighbors(self, x, y):
        """Get valid neighboring positions."""
        neighbors = []
        directions = [("up", (0, -1)), ("down", (0, 1)), ("left", (-1, 0)), ("right", (1, 0))]

        for _, (dx, dy) in directions:
            nx, ny = x + dx, y + dy
            if self.environment.is_within_bounds(nx, ny) and not self.environment.is_barrier(nx, ny):
                neighbors.append((nx, ny))

        return neighbors