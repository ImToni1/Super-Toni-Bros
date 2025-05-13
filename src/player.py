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

    def collide_with_platform(self, platform_rect):
        # Prvo provjeri općenito preklapanje pravokutnika
        if not self.rect.colliderect(platform_rect):
            return False

        # Uvjeti za slijetanje na vrh platforme:
        # 1. Igrač se kreće prema dolje (ili je bio stacionaran pa će gravitacija djelovati)
        # 2. Donji rub igrača je na ili ispod gornjeg ruba platforme
        # 3. Gornji rub igrača je iznad gornjeg ruba platforme (da potvrdimo da nije udarac odozdo ili sa strane previsoko)
        # 4. Donji rub igrača nije prošao *previše* ispod gornjeg ruba platforme (tolerancija za jedan korak brzine)
        
        is_moving_downwards = self.vel_y >= 0
        # Tolerancija (abs(self.vel_y) + 1) omogućuje da igrač malo "prođe" kroz vrh platforme prije nego se ispravi.
        # To pomaže kod diskretnih koraka i različitih brzina pada.
        is_bottom_colliding_with_top_surface = self.rect.bottom >= platform_rect.top and \
                                               self.rect.bottom <= platform_rect.top + abs(self.vel_y) + 1 
        is_top_above_platform_top = self.rect.top < platform_rect.top

        if is_moving_downwards and is_bottom_colliding_with_top_surface and is_top_above_platform_top:
            # Ako su vertikalni uvjeti za slijetanje zadovoljeni, provjeri horizontalnu poziciju
            player_center_x = self.rect.centerx
            platform_left_edge = platform_rect.left
            platform_right_edge = platform_rect.right

            if platform_left_edge < player_center_x < platform_right_edge:
                # Igrač je horizontalno podržan centrom iznad platforme
                self.rect.bottom = platform_rect.top  # Postavi igrača točno na vrh platforme
                self.vel_y = 0          # Zaustavi vertikalno kretanje
                self.on_ground = True   # Igrač je na tlu
                return True             # Uspješan sudar i prizemljenje
            else:
                # Horizontalno nije podržan, iako bi vertikalno mogao sletjeti.
                # Dopusti mu da propadne ako nije dobro centriran.
                # self.on_ground ostaje False (ili kakav je bio prije ove provjere)
                return False
                
        return False # Nije došlo do sudara koji bi rezultirao prizemljenjem na vrh.

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))