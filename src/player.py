import pygame
import os

class Player:
    def __init__(self, x, y, width, height):
        scale_factor = 1.5
        width = int(width * scale_factor)
        height = int(height * scale_factor)

        self.rect = pygame.Rect(x, y, width, height)
        self.vel_y = 0
        self.on_ground = False

        base_path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_path, "../images/Player.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

    def reset(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.on_ground = False

    def jump(self, jump_strength):
        self.vel_y = jump_strength
        self.on_ground = False

    def apply_gravity(self, gravity):
        self.vel_y += gravity
        self.rect.y += self.vel_y

    def collide_with_platform(self, platform):
        if self.rect.colliderect(platform):
            if self.vel_y > 0 and self.rect.bottom <= platform.bottom:
                self.rect.bottom = platform.top
                self.vel_y = 0
                self.on_ground = True
                return True
        return False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))