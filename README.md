# Super Toni Bros

Super Toni Bros is a simple platformer game built in Python using the `pygame` library. Game levels are now defined via external text files.

## Project Contents

* **`start.py`**: The main script to launch the game. It specifies the level file to be loaded.
* **`src/main.py`**: Contains the core game logic, including player movement, handling platforms loaded by `PlatformManager`, and the victory screen.
* **`src/player.py`**: Defines the `Player` class for handling player movement, jumping, and gravity.
* **`src/platforms.py`**: Defines the `PlatformManager` class for loading platforms from a level file, managing them, and setting the goal.
* **`src/level.txt`**: Text file defining the layout of platforms for a level.
* **`images/`**: Contains assets such as the background, player, platforms, ground, and victory screen.
* **`README.md`**: This document describing the project.

## How to Play

> [!IMPORTANT]
> **1. Prepare a Level File**
> * The game uses the `src/level.txt` file to define the level.
> * Inside this file, define each platform on a new line using the format: `x,y,width` (e.g., `400,500,150`). The platform height is fixed.
> * Lines starting with `#` will be treated as comments and ignored.

> [!NOTE]
> **2. Configure and Run the Game**
> * Ensure the `level_filepath` variable in `start.py` correctly points to `os.path.join(src_path, "level.txt")`.
> * Start the game by running:
>     ```bash
>     python start.py
>     ```

**3. Controls**:
* **Right Arrow (`→`)**: Move the player to the right (scrolls the platforms to the left).
* **Left Arrow (`←`)**: Move the player to the left (scrolls the platforms to the right).
* **Spacebar (`Space`)**: Jump (only works when the player is on the ground).

**4. Objective**:
* Reach the flag on the final platform (as defined by the level file) to win the game.

## About the Game

* **Gravity**: The player is affected by gravity and will fall if not on a platform.
* **Platforms**: Platform layouts are now loaded from level-specific text files. Platform height is predefined.
* **Victory Screen**: When the player reaches the goal, a "You Win!" screen is displayed along with the time taken to complete the game.

## Requirements

> [!IMPORTANT]
> * Python 3.x
> * `pygame` library

> [!TIP]
> Install `pygame` if it's not already installed:
> ```bash
> pip install pygame
> ```
