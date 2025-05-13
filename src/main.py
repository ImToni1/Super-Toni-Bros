import pygame
import sys
import os
from platforms import PlatformManager # Pretpostavljam da si primijenio prethodne izmjene za skaliranje slika platformi u platforms.py
from player import Player

LEVEL_FILEPATH = "level.txt" # U start.py se koristi level.txt, osiguraj konzistentnost ili koristi proslijeđeni argument

def run_game(level_filepath): # level_filepath se sada koristi kako je i namijenjeno
    pygame.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Super Toni Bros")

    base_path = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(base_path, "../images/Background.jpeg")
    background_image = pygame.image.load(background_path).convert()

    win_image_path = os.path.join(base_path, "../images/Winner's_scene.png")
    win_image = pygame.image.load(win_image_path).convert()
    win_image = pygame.transform.scale(win_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    FPS = 60
    gravity = 0.8
    jump_strength = -15
    speed = 5 # Brzina kretanja/scrollanja

    font = pygame.font.SysFont(None, 80)
    timer_font = pygame.font.SysFont(None, 35)

    player = Player(100, SCREEN_HEIGHT - 150, 50, 50)
    platform_manager = PlatformManager(SCREEN_WIDTH, SCREEN_HEIGHT, level_filepath)
    platform_manager.generate_platforms()

    # Inicijalizacija vremena na početku igre. Ovo se više neće resetirati.
    start_time = pygame.time.get_ticks()

    def reset_game():
        # Sada globalni 'start_time' dohvaćamo samo za čitanje, ne mijenjamo ga ovdje.
        # nonlocal player, platform_manager, start_time # start_time se više ne mijenja pa ga maknemo iz nonlocal ako se ne čita
        nonlocal player, platform_manager # Dovoljno je samo ovo dvoje specificirati kao nonlocal
        
        player.reset(100, SCREEN_HEIGHT - 150)
        # Ponovno inicijaliziraj PlatformManager da resetiraš platforme
        platform_manager = PlatformManager(SCREEN_WIDTH, SCREEN_HEIGHT, level_filepath)
        platform_manager.generate_platforms()
        # Linija "start_time = pygame.time.get_ticks()" je UKLONJENA
        # tako da se originalni 'start_time' s početka igre čuva.

    def show_victory_screen(elapsed_time):
        screen.blit(win_image, (0, 0))
        victory_text = font.render("You Win!", True, (0, 0, 0))
        # Formatiranje vremena da uvijek prikazuje dvije decimale
        time_text_str = f"Time: {elapsed_time:.2f} seconds"
        time_text = font.render(time_text_str, True, (0, 0, 0))

        screen.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN: # Izlazak na bilo koji pritisak
                    waiting = False # Prekini petlju čekanja da bi se vratio i završio run_game
            if not waiting: # Ako je waiting postavljen na False, izađi iz petlje
                break 
        # Nakon show_victory_screen, igra bi se trebala završiti ili vratiti u glavni meni (ako postoji)
        # Ovdje ćemo postaviti running na False da se igra završi nakon pobjede i prikaza ekrana.


    running = True
    game_won = False # Varijabla za praćenje stanja pobjede

    while running:
        clock.tick(FPS)
        
        # Izračunaj proteklo vrijeme samo ako igra nije pobijeđena
        if not game_won:
            current_ticks = pygame.time.get_ticks()
            elapsed_time = (current_ticks - start_time) / 1000

        for x_bg in range(0, SCREEN_WIDTH, background_image.get_width()):
            for y_bg in range(0, SCREEN_HEIGHT, background_image.get_height()):
                screen.blit(background_image, (x_bg, y_bg))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and player.on_ground:
            player.jump(jump_strength)

        player.apply_gravity(gravity)

        if player.rect.top > SCREEN_HEIGHT: # Igrač je pao
            reset_game()
            # Timer se NEĆE resetirati zbog promjene u reset_game()

        # Kretanje lijevo i desno
        scroll_offset = 0
        if keys[pygame.K_RIGHT]:
            scroll_offset = speed
        elif keys[pygame.K_LEFT]: # Koristi elif da se ne bi poništavali ako su obje pritisnute
            scroll_offset = -speed # Negativna vrijednost za pomicanje platformi udesno

        platform_manager.update_platforms(scroll_offset)

        player.on_ground = False
        for plat in platform_manager.platforms:
            if player.collide_with_platform(plat):
                player.on_ground = True # Postavi on_ground na True ako je detektirana kolizija
                break
        
        # Provjera pobjede
        if not game_won and platform_manager.goal and player.rect.colliderect(platform_manager.goal):
            game_won = True # Postavi da je igra pobijeđena
            # Vrijeme pobjede je elapsed_time izračunato u trenutku kolizije s ciljem
            victory_elapsed_time = elapsed_time 
            show_victory_screen(victory_elapsed_time)
            running = False # Završi glavnu petlju nakon prikaza pobjedničkog ekrana
            break # Izađi iz petlje odmah

        player.draw(screen)
        platform_manager.draw(screen)

        # Prikaz timera
        # Koristi victory_elapsed_time za prikaz na pobjedničkom ekranu, a elapsed_time za prikaz tijekom igre
        timer_display_value = victory_elapsed_time if game_won else elapsed_time
        timer_text = timer_font.render(f"Time: {timer_display_value:.2f} s", True, (0, 0, 0))
        screen.blit(timer_text, (10, 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()

