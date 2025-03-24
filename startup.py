from ursina import *

def create_startup_screen(start_game_callback):
    # Create a text element for the description of the game
    start_screen_text = Text(
        text="Welcome to AeroStrick!",
        color=color.white,
        scale=2,  # Adjust the scale to make it bigger
        origin=(0.5, 0.5),  # Center the text horizontally and vertically
        position=(0.25, 0.2),  # Adjust the vertical position to center
        enabled=True
    )

    # Create a "Start Game" button
    start_button = Button(
        text="Start Game",
        scale=(0.2, 0.1),  # Scale to make the button large enough
        position=(0, -0.1),  # Position just below the description
        color=color.green,
        on_click=start_game_callback,  # Call the start_game function on click
        text_color=color.white,
        highlight_color=color.light_gray
    )

    return start_screen_text, start_button
