import pygame
import os

class Player:
    def __init__(self, x, y, width, height):
        scale_factor = 1.5
        original_width = int(width * scale_factor)
        original_height = int(height * scale_factor)

        self.rect = pygame.Rect(x, y, original_width, original_height)
        self.vel_y = 0
        self.on_ground = False
        self.facing_left = False # Nova varijabla za praćenje smjera

        base_path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_path, "../images/Player.png")
        
        # Učitavanje originalne slike (okrenuta desno)
        self.image_right = pygame.image.load(image_path).convert_alpha()
        self.image_right = pygame.transform.scale(self.image_right, (original_width, original_height))
        
        # Kreiranje slike okrenute lijevo (zrcaljenjem)
        self.image_left = pygame.transform.flip(self.image_right, True, False) # True za horizontalno, False za vertikalno
        
        # Trenutna slika koja se koristi za crtanje
        self.image = self.image_right # Počinje okrenut desno

    def reset(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.on_ground = False
        self.facing_left = False # Resetiraj i smjer
        self.image = self.image_right # Vrati na originalnu sliku

    def jump(self, jump_strength):
        self.vel_y = jump_strength
        self.on_ground = False

    def apply_gravity(self, gravity):
        self.vel_y += gravity
        self.rect.y += self.vel_y

    def collide_with_platform(self, platform_rect):
        # Prvo provjeri općenito preklapanje pravokutnika
        if not self.rect.colliderect(platform_rect):
            return False

        is_moving_downwards = self.vel_y >= 0
        is_bottom_colliding_with_top_surface = self.rect.bottom >= platform_rect.top and \
                                               self.rect.bottom <= platform_rect.top + abs(self.vel_y) + 1 
        is_top_above_platform_top = self.rect.top < platform_rect.top

        if is_moving_downwards and is_bottom_colliding_with_top_surface and is_top_above_platform_top:
            player_center_x = self.rect.centerx
            platform_left_edge = platform_rect.left
            platform_right_edge = platform_rect.right

            if platform_left_edge < player_center_x < platform_right_edge:
                self.rect.bottom = platform_rect.top
                self.vel_y = 0
                self.on_ground = True
                return True
            else:
                return False
                
        return False

    # Nova metoda za ažuriranje smjera i slike
    def update_image_direction(self):
        if self.facing_left:
            self.image = self.image_left
        else:
            self.image = self.image_right

    def draw(self, screen):
        self.update_image_direction() # Ažuriraj sliku prije crtanja
        screen.blit(self.image, (self.rect.x, self.rect.y))