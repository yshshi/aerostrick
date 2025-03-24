# main.py
from ursina import *
from startup import create_startup_screen  # Import the startup screen
from player import Player
from enemies import EnemyManager
from obstacles import ObstacleManager
from shooting import ShootingManager

# Initialize the game
app = Ursina()

high_score = 0
score_text = Text(
    text="Score: 0",
    scale=1.5,
    color=color.white,
    position=(-0.85, 0.45),  # Top-left corner
    enabled=False  # Initially hidden
)

game_over_text = Text(
    text="Game Over!",
    scale=2,
    color=color.red,
    origin=(0.5, 0.5),  # Center the text horizontally and vertically
    position=(0.25, 0.2),
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

# Game components (initialized later)
player = None
obstacle_manager = None
enemy_manager = None
shooting_manager = None

game_started = False  # Flag to track if the game has started

# Function to initialize game components and start the game
def start_game():
    global player, obstacle_manager, enemy_manager, shooting_manager, game_started

    # Hide the start screen
    start_screen_text.enabled = False
    start_button.enabled = False

    # Initialize game components
    player = Player(show_game_over_screen)  # Pass the function to Player
    obstacle_manager = ObstacleManager()
    enemy_manager = EnemyManager()
    shooting_manager = ShootingManager(player)

    # Display score text and other gameplay elements
    score_text.enabled = True

    game_started = True  # Set the flag to True when the game starts

# Function to update score display
def update_score(score):
    score_text.text = f"Score: {score}"

# Function to show the game over screen
def show_game_over_screen():
    global high_score
    if shooting_manager.score > high_score:
        high_score = shooting_manager.score
        print(f"New high score: {high_score}")
    game_over_text.enabled = True
    restart_button.enabled = True
    quit_button.enabled = True

# Function to restart the game
def restart_game():
    global game_started
    # Reset player position
    player.entity.position = (0, -2, 0)  # Move player slightly below the center

    # Reset score
    shooting_manager.score = 0
    update_score(0)

    # Clear and destroy all enemies
    for enemy in enemy_manager.enemies:
        destroy(enemy)
    enemy_manager.enemies.clear()

    # Clear and destroy all bullets
    for bullet in enemy_manager.enemy_bullets:
        destroy(bullet)
    enemy_manager.enemy_bullets.clear()

    # Clear and destroy all obstacles
    for obstacle in obstacle_manager.obstacles:
        destroy(obstacle)
    obstacle_manager.obstacles.clear()

    # Hide the game over screen
    game_over_text.enabled = False
    restart_button.enabled = False
    quit_button.enabled = False

    game_started = False  # Reset the game started flag

# Function to quit the game
def quit_game():
    quit()

# Assign button actions
restart_button.on_click = restart_game
quit_button.on_click = quit_game

# Custom update function
def update():
    if game_started:  # Only update the game logic if the game has started
        if not game_over_text.enabled:  # Only update if the game is not over
            # Call the player's update method explicitly
            player.update(enemy_manager.enemies, obstacle_manager.obstacles)

            # Update obstacles and enemies
            obstacle_manager.update()
            enemy_manager.update(player)

            # Update shooting logic
            shooting_manager.update(enemy_manager.enemies)

            # Update score display
            update_score(shooting_manager.score)

            # Shoot when spacebar is pressed
            if held_keys['space']:
                shooting_manager.shoot(player.entity.forward)

            # Make enemies shoot at the player
            enemy_manager.shoot_at_player(player.entity.position)

# Create the startup screen (passing start_game as an argument)
start_screen_text, start_button = create_startup_screen(start_game)

# Run the game (startup screen will be shown initially)
app.run()
