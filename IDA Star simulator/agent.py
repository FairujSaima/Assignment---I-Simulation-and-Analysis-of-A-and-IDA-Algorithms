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
        """Find the nearest task using IDA*."""
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
        """IDA* pathfinding algorithm."""
        start = tuple(self.position)
        goal = target

       
        threshold = self.heuristic(start, goal)
        
        while True:
            path, cost, new_threshold = self.ida_star_search(start, goal, threshold)
            
            if path:
                return path, cost 
            elif new_threshold == float('inf'):
                return None  
            else:
                threshold = new_threshold  

    def ida_star_search(self, node, goal, threshold, path=None, g_cost=0):
        """Recursive depth-first search with heuristic pruning."""
        if path is None:
            path = [node]

        f_cost = g_cost + self.heuristic(node, goal)

        if f_cost > threshold:
            return None, None, f_cost  

        if node == goal:
            return path, g_cost, None  

        min_threshold = float('inf')
        neighbors = self.get_neighbors(*node)

        for neighbor in neighbors:
            if neighbor in path: 
                continue

            new_path = path + [neighbor]
            new_g_cost = g_cost + 1  

            result, result_cost, new_thresh = self.ida_star_search(
                neighbor, goal, threshold, new_path, new_g_cost
            )

            if result:  
                return result, result_cost, None
            
            if new_thresh is not None:
                min_threshold = min(min_threshold, new_thresh)

        return None, None, min_threshold  

    def heuristic(self, position, goal):
        """Manhattan distance heuristic."""
        return abs(position[0] - goal[0]) + abs(position[1] - goal[1])

    def get_neighbors(self, x, y):
        """Get valid neighboring positions."""
        neighbors = []
        directions = [("up", (0, -1)), ("down", (0, 1)), ("left", (-1, 0)), ("right", (1, 0))]

        for _, (dx, dy) in directions:
            nx, ny = x + dx, y + dy
            if self.environment.is_within_bounds(nx, ny) and not self.environment.is_barrier(nx, ny):
                neighbors.append((nx, ny))

        return neighbors