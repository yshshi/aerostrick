from ursina import *
from player import Player
from obstacles import ObstacleManager
from enemies import EnemyManager
from shooting import ShootingManager

# Initialize the game
app = Ursina()

# Function to show the game over screen
def show_game_over_screen():
    game_over_text.enabled = True
    restart_button.enabled = True
    quit_button.enabled = True

# Load game components
player = Player(show_game_over_screen)  # Pass the function to Player
obstacle_manager = ObstacleManager()
enemy_manager = EnemyManager()
shooting_manager = ShootingManager(player)

# Add a crosshair for aiming
crosshair = Entity(
    model='quad',  # Simple 2D quad for the crosshair
    color=color.red,  # Change color to red for better visibility
    scale=0.02,  # Make it smaller
    parent=camera.ui,  # Attach to the UI layer
    position=(0, 0, 0)  # Center of the screen
)

# Add an aiming line
aiming_line = Entity(
    model='line',  # Use the 'line' model
    color=color.white,
    parent=player.entity,  # Attach to the player
    scale=(0.1, 0.1, 10),  # Adjust the scale to make it visible
    rotation=(0, 0, 0)  # Align with the player's forward direction
)

# Game over screen
game_over_text = Text(
    text="Game Over!",
    scale=2,
    color=color.red,
    position=(0, 0.1),
    enabled=False  # Hidden by default
)
restart_button = Button(
    text="Restart",
    scale=0.1,
    position=(0, -0.1),
    enabled=False  # Hidden by default
)
quit_button = Button(
    text="Quit",
    scale=0.1,
    position=(0, -0.3),
    enabled=False  # Hidden by default
)

# Function to restart the game
def restart_game():
    player.entity.position = (0, 0, 0)  # Reset player position
    enemy_manager.enemies.clear()  # Clear all enemies
    obstacle_manager.obstacles.clear()  # Clear all obstacles
    shooting_manager.bullets.clear()  # Clear all bullets
    game_over_text.enabled = False
    restart_button.enabled = False
    quit_button.enabled = False

# Function to quit the game
def quit_game():
    quit()

# Assign button actions
restart_button.on_click = restart_game
quit_button.on_click = quit_game

# Custom update function
def update():
    if not game_over_text.enabled:  # Only update if the game is not over
        # Call the player's update method explicitly
        player.update(enemy_manager.enemies, obstacle_manager.obstacles)

        # Update obstacles and enemies
        obstacle_manager.update()
        enemy_manager.update()

        # Update shooting logic
        shooting_manager.update(enemy_manager.enemies)

        # Shoot when spacebar is pressed
        if held_keys['space']:
            shooting_manager.shoot()

        # Update aiming line position and direction
        aiming_line.position = player.entity.position
        aiming_line.rotation = player.entity.rotation

# Run the game
app.run()