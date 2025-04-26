# Super Toni Bros

Super Toni Bros is a simple platformer game built in Python using the `pygame` library.

## Project Contents

- **`start.py`**: The main script to launch the game.
- **`src/main.py`**: Contains the core game logic, including player movement, platform management, and the victory screen.
- **`src/player.py`**: Defines the `Player` class for handling player movement, jumping, and gravity.
- **`src/platforms.py`**: Defines the `PlatformManager` class for generating and managing platforms and the goal.
- **`images/`**: Contains assets such as the background, player, platforms, ground, and victory screen.

## How to Play

1. **Run the Game**:
   - Start the game by running:
     ```bash
     python start.py
     ```
   - This script initializes the game with a predefined number of platforms, height variation, and spacing.

2. **Controls**:
   - **Right Arrow (`→`)**: Move the player to the right.
   - **Spacebar (`Space`)**: Jump (only works when the player is on the ground).

3. **Objective**:
   - Reach the flag on the final platform to win the game.

## About the Game

- **Gravity**: The player is affected by gravity and will fall if not on a platform.
- **Platforms**: Platforms are randomly generated with configurable height variation and spacing.
- **Victory Screen**: When the player reaches the goal, a "You Win!" screen is displayed along with the time taken to complete the game.

## Directory Structure
Super-Toni-Bros/ ├── images/ │ ├── Background.jpeg │ ├── Player.png │ ├── Platforms.png │ ├── Ground.png │ └── Winner's_scene.png ├── src/ │ ├── main.py │ ├── player.py │ └── platforms.py ├── start.py └── README.md



## Requirements

- Python 3.x
- [pygame](http://_vscodecontentref_/1) library

Install [pygame](http://_vscodecontentref_/2) if it's not already installed:
```bash
pip install pygame