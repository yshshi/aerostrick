from ursina import *

class Player:
    def __init__(self, show_game_over_screen):
        # Create a player entity
        self.entity = Entity(
            model='sphere',  # Player is an orange sphere
            color=color.orange,
            scale=1,
            position=(0, 0, 0),
            collider='sphere'
        )
        self.show_game_over_screen = show_game_over_screen  # Store the function

    def update(self, enemies, obstacles):
        # Movement using arrow keys
        if held_keys['left arrow']:  # Move left
            self.entity.x -= 0.1
        if held_keys['right arrow']:  # Move right
            self.entity.x += 0.1
        if held_keys['up arrow']:  # Move up
            self.entity.y += 0.1
        if held_keys['down arrow']:  # Move down
            self.entity.y -= 0.1

        # Check for collisions with enemies
        for enemy in enemies:
            if self.entity.intersects(enemy):
                print("Player hit an enemy! Game Over!")
                self.show_game_over_screen()  # Call the function
                return  # Stop further updates

        # Check for collisions with obstacles
        for obstacle in obstacles:
            if self.entity.intersects(obstacle):
                print("Player hit an obstacle! Game Over!")
                self.show_game_over_screen()  # Call the function
                return  # Stop further updates