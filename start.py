import os
import sys

src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
sys.path.append(src_path)

num_platforms = 7  # Broj platformi
height_variation = 10  # Visinska varijacija platformi
platform_spacing = 300 # Razmak između platformi

import main
main.run_game(num_platforms, height_variation,platform_spacing )

