from ursina import *

class ShootingManager:
    def __init__(self, player):
        self.player = player
        self.bullets = []  # List to store active bullets

    def shoot(self):
        # Create a bullet at the player's position
        bullet = Entity(
            model='sphere',  # Bullet is a small sphere
            color=color.yellow,
            scale=0.2,
            position=self.player.entity.position,  # Use player's entity position
            collider='sphere'
        )
        self.bullets.append(bullet)
        print("Bullet shot!")  # Debugging

    def update(self, enemies):
        # Move bullets forward
        for bullet in self.bullets[:]:  # Iterate over a copy of the list
            bullet.z += 1.0  # Increased bullet speed

            # Check for collisions with enemies
            for enemy in enemies[:]:  # Iterate over a copy of the list
                if bullet.intersects(enemy):
                    print("Enemy hit!")  # Debugging
                    self.bullets.remove(bullet)  # Remove bullet from the list
                    enemies.remove(enemy)  # Remove enemy from the list
                    destroy(bullet)  # Destroy the bullet
                    destroy(enemy)  # Destroy the enemy
                    break  # Exit the loop after destroying the enemy

            # Remove bullet if it goes off-screen
            if bullet.z > 20:
                self.bullets.remove(bullet)
                destroy(bullet)
                print("Bullet destroyed!")  # Debugging