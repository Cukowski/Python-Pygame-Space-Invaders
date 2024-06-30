# Python-Pygame-Space-Invaders

## Description
This is a simple Space Invaders game implemented in Python using the Pygame library. The game features player-controlled ships, alien invaders, and bullets. Your objective is to defend Earth by shooting down the invading aliens.

## Features
Player-controlled ship movement
Alien invaders with randomized movement
Bullets for shooting down aliens
Score tracking
Installation
Make sure you have Python installed (Download Python).
Install the Pygame library:
pip install pygame

## How to Play
Run the game:
python main.py
* The game is played by right, left arrow keys and space button.
* You can move around the screen by arrow keys and shoot by space.
* Enemies will appear on the top of the screen and shoot randomly.
* If an enemy hits you, your health score goes down.
* When all enemies are killed, you win! Game is over.

Use the arrow keys to move your ship left and right.
Press the spacebar to shoot bullets.
Shoot down as many aliens as you can to earn points.

### File Structure
settings.py: Define game variables (e.g., screen dimensions, speeds).
main.py: Main game loop and initialization.
world.py: Handles game mechanics (aliens, bullets, collisions).
display.py: Manages the game window and rendering.
alien.py: Alien class.
ship.py: Player ship class.
bullet.py: Bullet class.

## Acknowledgments
Inspired by the classic Space Invaders arcade game.
Thanks to the Pygame community for the library.

* On the V1.2 you can replay by pressing enter (Still working on it, doesn't function yet)
