from ursina import *

class ShootingManager:
    def __init__(self, player):
        self.player = player
        self.bullets = []  # List to store active bullets

    def shoot(self, direction):
        # Create a bullet at the player's position
        bullet = Entity(
            model='sphere',  # Bullet is a small sphere
            color=color.yellow,
            scale=0.2,
            position=self.player.entity.position,  # Use player's entity position
            collider='sphere'
        )
        # Set the bullet's direction to match the aiming indicator's direction
        bullet.direction = direction
        self.bullets.append(bullet)
        print("Bullet shot!")  # Debugging

    def update(self, enemies):
        bullets_to_remove = []  # Store bullets to remove
        enemies_to_remove = []  # Store enemies to remove

        # Move bullets forward
        for bullet in self.bullets[:]:  
            if not bullet.enabled:  # Skip if bullet is already destroyed
                continue

            # Move the bullet in the direction it was shot
            bullet.position += bullet.direction * 1.0  # Adjust speed as needed

            # Check for collisions with enemies
            for enemy in enemies[:]:  
                if not enemy.enabled:  
                    continue

                if bullet.intersects(enemy):
                    print("Enemy hit!")  
                    bullets_to_remove.append(bullet)  # Mark bullet for removal
                    enemies_to_remove.append(enemy)  # Mark enemy for removal
                    break  

            # Remove bullet if it goes off-screen
            if bullet.enabled and bullet.z > 20:
                bullets_to_remove.append(bullet)  

        # Remove bullets outside the loop to prevent modifying the list while iterating
        for bullet in bullets_to_remove:
            if bullet in self.bullets:  # Ensure bullet is still in the list
                self.bullets.remove(bullet)
                destroy(bullet)  
                print("Bullet destroyed!")  

        # Remove enemies outside the loop to prevent modifying the list while iterating
        for enemy in enemies_to_remove:
            if enemy in enemies:  # Ensure enemy is still in the list
                enemies.remove(enemy)
                destroy(enemy)  
                print("Enemy destroyed!")  