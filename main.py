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
            shooting_manager.shoot()

        # Update aiming line position and direction
        aiming_line.position = player.entity.position
        aiming_line.rotation = player.entity.rotation

        # Ensure the aiming line points forward
        aiming_line.look_at(player.entity.position + player.entity.forward)

# Run the game
app.run()