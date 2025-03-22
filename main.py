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
    player.entity.position = (0, -2, 0)  # Move player slightly below the center

    # Clear and destroy all enemies
    for enemy in enemy_manager.enemies:
        destroy(enemy)
    enemy_manager.enemies.clear()

    # Clear and destroy all bullets
    for bullet in enemy_manager.enemy_bullets:
        destroy(bullet)
    enemy_manager.enemy_bullets.clear()

    # Clear and destroy all trail segments
    for segment in enemy_manager.trail_segments:
        destroy(segment)
    enemy_manager.trail_segments.clear()

    # Clear and destroy all obstacles (if applicable)
    for obstacle in obstacle_manager.obstacles:
        destroy(obstacle)
    obstacle_manager.obstacles.clear()

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

# Tilt the camera slightly downward without changing its position
# camera.rotation_x = 15  # Tilt the camera slightly downward

# Custom update function
def update():
    if not game_over_text.enabled:  # Only update if the game is not over
        # Call the player's update method explicitly
        player.update(enemy_manager.enemies, obstacle_manager.obstacles)

        # Update obstacles and enemies
        obstacle_manager.update()
        enemy_manager.update(player)  # Pass the player object, not just the position

        # Update shooting logic
        shooting_manager.update(enemy_manager.enemies)

        # Shoot when spacebar is pressed
        if held_keys['space']:
            shooting_manager.shoot(player.entity.forward)  # Shoot in the direction of the player's forward vector

        # Make enemies shoot at the player
        enemy_manager.shoot_at_player(player.entity.position)

# Set initial player position slightly below the center
player.entity.position = (0, -2, 0)

# Run the game
app.run()