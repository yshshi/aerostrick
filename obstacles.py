from ursina import *
from random import randint

class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def create_obstacle(self):
        obstacle = Entity(
            model='sphere',  # Obstacle is a red sphere
            color=color.red,
            scale=1,
            position=(randint(-10, 10), randint(1, 5), randint(20, 30)),
            collider='sphere'
        )
        self.obstacles.append(obstacle)

    def update(self):
        for obstacle in self.obstacles:
            obstacle.z -= 0.1  # Move obstacle toward the player
            if obstacle.z < -10:  # Remove obstacle if it goes past the player
                self.obstacles.remove(obstacle)
                destroy(obstacle)

        # Generate new obstacles periodically
        if len(self.obstacles) < 5:  # Limit the number of obstacles
            self.create_obstacle()