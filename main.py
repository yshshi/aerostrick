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

# Add a crosshair for aiming (fixed at the center of the screen)
crosshair = Entity(
    model='quad',  # Simple 2D quad for the crosshair
    color=color.white,
    scale=0.02,
    parent=camera.ui,  # Attach to the UI layer
    position=(0, 0, 0)  # Center of the screen
)

# Add an aiming indicator (crosshair-like shape: -|-)
aiming_indicator = Entity(
    model=None,  # No base model, we'll add custom shapes
    parent=player.entity,  # Attach to the player
    position=(0, 0, 2),  # Position in front of the player
    rotation=(0, 0, 0)  # Align with the player's forward direction
)

# Add horizontal line (-)
horizontal_line = Entity(
    parent=aiming_indicator,
    model='cube',
    color=color.white,
    scale=(0.5, 0.02, 0.02),  # Thin and long horizontal line
    position=(0, 0, 0)  # Center of the crosshair
)

# Add vertical line (|)
vertical_line = Entity(
    parent=aiming_indicator,
    model='cube',
    color=color.white,
    scale=(0.02, 0.5, 0.02),  # Thin and long vertical line
    position=(0, 0, 0)  # Center of the crosshair
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
    # Reset player position
    player.entity.position = (0, 0, 0)

    # Clear and destroy all enemies
    for enemy in enemy_manager.enemies:
        destroy(enemy)
    enemy_manager.enemies.clear()

    # Clear and destroy all obstacles
    for obstacle in obstacle_manager.obstacles:
        destroy(obstacle)
    obstacle_manager.obstacles.clear()

    # Clear and destroy all bullets
    for bullet in shooting_manager.bullets:
        destroy(bullet)
    shooting_manager.bullets.clear()

    # Hide the game over screen
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
            shooting_manager.shoot(aiming_indicator.forward)  # Shoot in the direction of the aiming indicator

        # Update aiming indicator position and direction
        aiming_indicator.position = player.entity.position + player.entity.forward * 2  # Move in front of the player
        aiming_indicator.rotation = player.entity.rotation  # Align with the player's forward direction

# Run the game
app.run()