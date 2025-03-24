# startup.py
from ursina import *

# Function to create the startup screen
def create_startup_screen(start_game):
    # Display the game description text
    start_screen_text = Text(
        text="Welcome to the Ultimate Space Battle Game!\n\nShoot down the enemies, avoid obstacles, and try to get the highest score!",
        scale=1.5,
        color=color.white,
        position=(0, 0.3),
        enabled=True
    )

    # Create the Start Game button
    start_button = Button(
        text="Start Game",
        scale=0.1,
        position=(0, -0.3),
        on_click=start_game  # Pass the function that starts the game
    )

    return start_screen_text, start_button
