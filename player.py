from ursina import *

class Player:
    def __init__(self, show_game_over_screen):
        # Create the player entity with an aeroplane model
        self.entity = Entity(
            model='cube',  # Temporarily use a cube for debugging
            texture='white_cube',
            color=color.blue,
            scale=(1, 1, 1),  # Adjust scale to fit the aeroplane model
            position=(0, -2, 0),  # Position slightly below the center
            rotation=(0, 0, 0),  # Initial rotation
            collider='box'  # Use a box collider for simplicity
        )
        self.show_game_over_screen = show_game_over_screen  # Store the function
        print("Player created!")  # Debugging

    def update(self, enemies, obstacles):
        # Movement using arrow keys
        if held_keys['left arrow']:  # Move left
            self.entity.x -= 0.1
            self.entity.rotation_z = 15  # Tilt left
        elif held_keys['right arrow']:  # Move right
            self.entity.x += 0.1
            self.entity.rotation_z = -15  # Tilt right
        else:
            self.entity.rotation_z = 0  # Reset tilt when not moving left/right

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