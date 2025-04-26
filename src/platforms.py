import pygame
import random
import os

class PlatformManager:
    def __init__(self, screen_width, screen_height, num_platforms=10, height_variation=10, platform_spacing=300):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.num_platforms = num_platforms
        self.height_variation = height_variation 
        self.platform_spacing = platform_spacing  
        self.platforms = []
        self.goal = None

        base_path = os.path.dirname(os.path.abspath(__file__))
        self.platform_image = pygame.image.load(os.path.join(base_path, "../images/platforms.png")).convert_alpha()
        self.ground_image = pygame.image.load(os.path.join(base_path, "../images/ground.png")).convert_alpha()
        self.flag_image = pygame.image.load(os.path.join(base_path, "../images/flag.png")).convert_alpha()
        self.flag_image = pygame.transform.scale(self.flag_image, (160, 160))  

    def generate_platforms(self):
        starting_ground = pygame.Rect(0, self.screen_height - 50, 300, 50)
        self.platforms.append(starting_ground)

        predefined_platforms = []
        base_y = self.screen_height - 100
        x_position = 400

        for i in range(self.num_platforms):
            y_variation = random.randint(-self.height_variation, self.height_variation)
            platform = pygame.Rect(x_position, base_y + y_variation, 150, 20)
            predefined_platforms.append(platform)
            x_position += self.platform_spacing  

        self.platforms.extend(predefined_platforms)

        if not self.goal:
            target_platform = self.platforms[-1]
            goal_width = 160  
            goal_height = 160  
            goal_x = target_platform.x + (target_platform.width - goal_width) // 2
            goal_y = target_platform.y - goal_height
            self.goal = pygame.Rect(goal_x, goal_y, goal_width, goal_height)

    def update_platforms(self, scroll_offset):
        for platform in self.platforms:
            platform.x -= scroll_offset
        if self.goal:
            self.goal.x -= scroll_offset

    def draw(self, screen):
        starting_ground = self.platforms[0]
        screen.blit(self.ground_image, (starting_ground.x, starting_ground.y))

        for platform in self.platforms[1:]:
            screen.blit(self.platform_image, (platform.x, platform.y))

        if self.goal:
            screen.blit(self.flag_image, (self.goal.x, self.goal.y))