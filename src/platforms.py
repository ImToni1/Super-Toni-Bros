import pygame
import os

class PlatformManager:
    FIXED_PLATFORM_HEIGHT = 30

    def __init__(self, screen_width, screen_height, level_filepath):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level_filepath = level_filepath
        self.platforms = []
        self.goal = None

        base_path = os.path.dirname(os.path.abspath(__file__))
        self.platform_image_original = pygame.image.load(os.path.join(base_path, "../images/Platforms.png")).convert_alpha()
        self.ground_image_original = pygame.image.load(os.path.join(base_path, "../images/Ground.png")).convert_alpha()
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
                        if len(parts) == 3: # Format: x,y,sirina
                            try:
                                x = int(parts[0])
                                y = int(parts[1])
                                width = int(parts[2])
                                height = PlatformManager.FIXED_PLATFORM_HEIGHT
                                loaded_platforms.append(pygame.Rect(x, y, width, height))
                            except ValueError:
                                print(f"Preskačem neispravan redak u {self.level_filepath}: {line}")
                        else:
                            print(f"Preskačem redak s netočnim brojem vrijednosti u {self.level_filepath}: {line}. Očekivani format: x,y,sirina")
        except FileNotFoundError:
            print(f"GREŠKA: Datoteka s razinom '{self.level_filepath}' nije pronađena.")
        return loaded_platforms

    def generate_platforms(self):
        self.platforms = []
        
        # Definicije za početnu platformu
        start_ground_initial_x = -200 # Koliko se platforma proteže lijevo izvan ekrana na početku
        start_ground_visible_width = 300 # Širina dijela platforme koji je vidljiv na početku
        start_ground_width = start_ground_visible_width + abs(start_ground_initial_x)
        
        starting_ground_y = self.screen_height - 50
        starting_ground_height = 50
        
        starting_ground = pygame.Rect(start_ground_initial_x, starting_ground_y, start_ground_width, starting_ground_height)
        self.platforms.append(starting_ground) # Index 0: Početna platforma

        # Desni nevidljivi zid (na kraju početne platforme)
        right_invisible_wall_width = 10
        right_invisible_wall_height = starting_ground.height # Može biti i self.screen_height ako želiš da je visok
        right_invisible_wall_x = starting_ground.right
        right_invisible_wall_y = starting_ground.top # Ako je visok, y bi bio 0
        # Ako želite da desni zid bude visok:
        # right_invisible_wall_y = 0
        # right_invisible_wall_height = self.screen_height
        right_invisible_wall = pygame.Rect(right_invisible_wall_x, right_invisible_wall_y, right_invisible_wall_width, right_invisible_wall_height)
        self.platforms.append(right_invisible_wall) # Index 1: Desni nevidljivi zid

        # Lijevi crveni zid
        left_wall_width = 10 # Širina lijevog zida

        # --- POZICIJA LIJEVOG ZIDA (lijevo-desno) ---
        # Ovdje možeš pomicati zid lijevo ili desno.
        # Trenutno je postavljen da bude odmah lijevo od početne platforme.
        # starting_ground.left je lijevi rub početne platforme (npr. -200)
        # left_wall_x = starting_ground.left - left_wall_width  postavlja zid odmah do platforme.
        # Za pomicanje udesno, povećaj vrijednost (npr. starting_ground.left - left_wall_width + 50).
        # Za pomicanje ulijevo, smanji vrijednost (npr. starting_ground.left - left_wall_width - 50).
        # Ili postavi fiksnu x koordinatu, npr. left_wall_x = -250
        left_wall_x = (starting_ground.left - left_wall_width) + 150
        # --- KRAJ SEKCIJE ZA POZICIJU ZIDA ---

        # Visina lijevog zida - ide do vrha ekrana
        left_wall_y = 0 # Počinje od vrha ekrana
        left_wall_height = self.screen_height # Proteže se do dna ekrana
        
        left_wall = pygame.Rect(left_wall_x, left_wall_y, left_wall_width, left_wall_height)
        self.platforms.append(left_wall) # Index 2: Lijevi zid (sada crveni i visok)

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
            print("Nema platformi učitanih iz datoteke, cilj nije automatski postavljen.")

    def update_platforms(self, scroll_offset):
        for platform in self.platforms:
            platform.x -= scroll_offset
        if self.goal:
            self.goal.x -= scroll_offset

    def draw(self, screen):
        if not self.platforms:
            return

        RED = (255, 0, 0)

        if len(self.platforms) > 0:
            ground_platform_rect = self.platforms[0]
            # Ovdje možeš dodati logiku za ponavljanje teksture ako želiš
            scaled_ground_image = pygame.transform.scale(self.ground_image_original, (ground_platform_rect.width, ground_platform_rect.height))
            screen.blit(scaled_ground_image, (ground_platform_rect.x, ground_platform_rect.y))

       

        # Lijevi zid (self.platforms[2]) - CRVENI I VIDLJIV
        if len(self.platforms) > 0: 
            pass

        for i in range(3, len(self.platforms)): 
            platform_rect = self.platforms[i]
            scaled_platform_image = pygame.transform.scale(self.platform_image_original, (platform_rect.width, platform_rect.height))
            screen.blit(scaled_platform_image, (platform_rect.x, platform_rect.y))
            
        if self.goal:
            screen.blit(self.flag_image, (self.goal.x, self.goal.y))