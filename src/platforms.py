import pygame
import os

class PlatformManager:
    def __init__(self, screen_width, screen_height, level_filepath):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level_filepath = level_filepath
        self.platforms = []
        self.goal = None

        base_path = os.path.dirname(os.path.abspath(__file__))
        self.platform_image = pygame.image.load(os.path.join(base_path, "../images/Platforms.png")).convert_alpha()
        self.ground_image = pygame.image.load(os.path.join(base_path, "../images/Ground.png")).convert_alpha()
        self.flag_image = pygame.image.load(os.path.join(base_path, "../images/Flag.png")).convert_alpha()
        self.flag_image = pygame.transform.scale(self.flag_image, (160, 160))

    def _load_platforms_from_file(self):
        loaded_platforms = []
        try:
            with open(self.level_filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split(',')
                        if len(parts) == 4:
                            try:
                                x = int(parts[0])
                                y = int(parts[1])
                                width = int(parts[2])
                                height = int(parts[3])
                                loaded_platforms.append(pygame.Rect(x, y, width, height))
                            except ValueError:
                                print(f"Skipping malformed line in {self.level_filepath}: {line}")
                        else:
                            print(f"Skipping line with incorrect number of values in {self.level_filepath}: {line}")
        except FileNotFoundError:
            print(f"ERROR: Level file '{self.level_filepath}' not found.")
        return loaded_platforms

    def generate_platforms(self):
        self.platforms = []
        starting_ground = pygame.Rect(0, self.screen_height - 50, 300, 50)
        self.platforms.append(starting_ground)
        platforms_from_file = self._load_platforms_from_file()
        self.platforms.extend(platforms_from_file)

        if platforms_from_file and not self.goal:
            target_platform = platforms_from_file[-1]
            goal_width = 160
            goal_height = 160
            goal_x = target_platform.x + (target_platform.width - goal_width) // 2
            goal_y = target_platform.y - goal_height
            self.goal = pygame.Rect(goal_x, goal_y, goal_width, goal_height)
        elif not platforms_from_file and not self.goal:
            print("No platforms loaded from file, goal not automatically set on the last platform.")

    def update_platforms(self, scroll_offset):
        for platform in self.platforms:
            platform.x -= scroll_offset
        if self.goal:
            self.goal.x -= scroll_offset

    def draw(self, screen):
        if self.platforms and self.platforms[0].width == 300 and self.platforms[0].height == 50:
            screen.blit(self.ground_image, (self.platforms[0].x, self.platforms[0].y))
            for platform in self.platforms[1:]:
                screen.blit(self.platform_image, (platform.x, platform.y))
        else:
            for platform in self.platforms:
                screen.blit(self.platform_image, (platform.x, platform.y))

        if self.goal:
            screen.blit(self.flag_image, (self.goal.x, self.goal.y))