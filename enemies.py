from ursina import *
from random import randint

class EnemyManager:
    def __init__(self):
        self.enemies = []

    def create_enemy(self):
        enemy = Entity(
            model='cube',  # Enemy is now a blue cube
            color=color.blue,
            scale=1,
            position=(randint(-10, 10), randint(1, 5), randint(20, 30)),
            collider='box'
        )
        self.enemies.append(enemy)

    def update(self):
        for enemy in self.enemies:
            enemy.z -= 0.1  # Move enemy toward the player
            if enemy.z < -10:  # Remove enemy if it goes past the player
                self.enemies.remove(enemy)
                destroy(enemy)

        # Generate new enemies periodically
        if len(self.enemies) < 3:  # Limit the number of enemies
            self.create_enemy()