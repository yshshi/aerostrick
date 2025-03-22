from ursina import *
from random import randint, random
import time  # Import the time module

class EnemyManager:
    def __init__(self):
        self.enemies = []
        self.enemy_bullets = []
        self.trail_segments = []  # List to store all trail segments
        self.shoot_cooldown = 3.0  # Increased cooldown time in seconds (5 seconds)

    def create_enemy(self):
        enemy = Entity(
            model='cube',  # Replace with a 3D airplane model
            color=color.blue,
            scale=1,
            position=(randint(-10, 10), randint(1, 5), randint(20, 30)),
            collider='box'
        )
        enemy.last_shot_time = 0  # Track the last time this enemy shot a bullet
        self.enemies.append(enemy)

    def shoot_at_player(self, player_position):
        current_time = time.time()  # Use time.time() to get the current time
        for enemy in self.enemies:
            # Check if enough time has passed since the last shot
            if current_time - enemy.last_shot_time >= self.shoot_cooldown:
                # Randomly decide if the enemy should shoot
                if random() < 0.5:  # Adjust probability as needed (e.g., 50% chance)
                    bullet = Entity(
                        model='sphere',
                        color=color.red,
                        scale=0.2,
                        position=enemy.position,
                        collider='sphere'
                    )
                    bullet.direction = (player_position - enemy.position).normalized()
                    self.enemy_bullets.append(bullet)

                    # Add a trail effect to the bullet
                    bullet.trail = []  # List to store trail segments
                    enemy.last_shot_time = current_time  # Update the last shot time
                    print("Enemy bullet created!")

    def update(self, player):
        # Move enemies
        for enemy in self.enemies:
            enemy.z -= 0.1
            if enemy.z < -10:
                self.enemies.remove(enemy)
                destroy(enemy)

        # Move bullets
        for bullet in self.enemy_bullets[:]:
            if not bullet.enabled:
                continue

            # Move the bullet
            bullet.position += bullet.direction * 0.1  # Reduced speed

            # Add a trail segment
            trail_segment = Entity(
                model='sphere',
                color=color.red,
                scale=0.1,
                position=bullet.position,
                alpha=0.5  # Semi-transparent
            )
            bullet.trail.append(trail_segment)
            self.trail_segments.append(trail_segment)  # Add to global trail segments list

            # Fade out and remove old trail segments
            for segment in bullet.trail:
                segment.alpha -= 0.02  # Fade out over time
                if segment.alpha <= 0:
                    bullet.trail.remove(segment)
                    self.trail_segments.remove(segment)  # Remove from global trail segments list
                    destroy(segment)

            # Check for collisions with the player
            if bullet.intersects(player.entity):
                print("Player hit by enemy bullet! Game Over!")
                player.show_game_over_screen()
                self.enemy_bullets.remove(bullet)
                destroy(bullet)
                break

            # Remove bullet if it goes off-screen
            if bullet.z < -10 or bullet.z > 20:
                self.enemy_bullets.remove(bullet)
                destroy(bullet)

        # Spawn new enemies
        if len(self.enemies) < 3:
            self.create_enemy()