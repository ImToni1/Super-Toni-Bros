import os
import sys

src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
sys.path.append(src_path)

level_filepath = os.path.join(src_path, "level.txt")

import main
main.run_game(level_filepath) 