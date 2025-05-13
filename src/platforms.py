import pygame
import os

class PlatformManager:
    FIXED_PLATFORM_HEIGHT = 0

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
        
        # 1. Početna platforma (tlo)
        starting_ground = pygame.Rect(0, self.screen_height - 50, 300, 50)
        self.platforms.append(starting_ground) # Index 0

        # 2. Nevidljivi zid na kraju početne platforme
        # Postavlja se odmah desno od starting_ground
        # Visina zida može biti ista kao visina starting_ground (ili visina igrača)
        invisible_wall_width = 10 # Mala širina za zid
        invisible_wall_height = starting_ground.height # Neka bude iste visine kao tlo
        invisible_wall_x = starting_ground.right
        invisible_wall_y = starting_ground.top
        
        invisible_wall = pygame.Rect(invisible_wall_x, invisible_wall_y, invisible_wall_width, invisible_wall_height)
        self.platforms.append(invisible_wall) # Index 1: Ovo je nevidljivi zid

        # 3. Platforme učitane iz level.txt datoteke
        platforms_from_file = self._load_platforms_from_file()
        self.platforms.extend(platforms_from_file) # Ove platforme počinju od indeksa 2

        # Postavljanje cilja na zadnjoj platformi iz datoteke (platforms_from_file)
        if platforms_from_file and not self.goal:
            target_platform = platforms_from_file[-1] # Uzmi zadnju iz originalno učitanih
            goal_width = 160
            goal_height = 160
            goal_x = target_platform.x + (target_platform.width - goal_width) // 2
            goal_y = target_platform.y - goal_height 
            self.goal = pygame.Rect(goal_x, goal_y, goal_width, goal_height)
        elif not platforms_from_file and not self.goal: # Ako nema platformi iz datoteke
             # Ako nema platformi iz datoteke, a starting_ground i invisible_wall postoje,
             # cilj bi se mogao postaviti na starting_ground ili nigdje.
             # Trenutna logika ga ne postavlja ako nema platformi iz datoteke.
            print("Nema platformi učitanih iz datoteke, cilj nije automatski postavljen.")


    def update_platforms(self, scroll_offset):
        for platform in self.platforms:
            platform.x -= scroll_offset
        if self.goal:
            self.goal.x -= scroll_offset

    def draw(self, screen):
        if not self.platforms:
            return

        # 1. Iscrtaj početnu platformu (tlo) - self.platforms[0]
        ground_platform_rect = self.platforms[0]
        scaled_ground_image = pygame.transform.scale(self.ground_image_original, (ground_platform_rect.width, ground_platform_rect.height))
        screen.blit(scaled_ground_image, (ground_platform_rect.x, ground_platform_rect.y))

        # 2. NE ISCRTAVAJ nevidljivi zid (self.platforms[1])

        # 3. Iscrtaj sve ostale platforme (one učitane iz level.txt)
        # One se nalaze od indeksa 2 nadalje
        for i in range(2, len(self.platforms)):
            platform_rect = self.platforms[i]
            scaled_platform_image = pygame.transform.scale(self.platform_image_original, (platform_rect.width, platform_rect.height))
            screen.blit(scaled_platform_image, (platform_rect.x, platform_rect.y))
            
        if self.goal:
            screen.blit(self.flag_image, (self.goal.x, self.goal.y))