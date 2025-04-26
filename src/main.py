import pygame
import sys
import os
from platforms import PlatformManager
from player import Player  

def run_game(num_platforms, height_variation,platform_spacing):  
    pygame.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Super Toni Bros")


    base_path = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(base_path, "../images/background.jpeg")
    background_image = pygame.image.load(background_path).convert()

    clock = pygame.time.Clock()
    FPS = 60
    gravity = 0.8
    jump_strength = -15
    speed = 5

    player = Player(100, SCREEN_HEIGHT - 150, 50, 50)


    platform_manager = PlatformManager(SCREEN_WIDTH, SCREEN_HEIGHT, num_platforms, height_variation=height_variation, platform_spacing=platform_spacing)
    platform_manager.generate_platforms()

    def reset_game():
        nonlocal player, platform_manager
        player.reset(100, SCREEN_HEIGHT - 150)
        platform_manager = PlatformManager(SCREEN_WIDTH, SCREEN_HEIGHT, num_platforms, height_variation=height_variation, platform_spacing=platform_spacing)
        platform_manager.generate_platforms()

    running = True
    while running:
        clock.tick(FPS)
        for x in range(0, SCREEN_WIDTH, background_image.get_width()):
            for y in range(0, SCREEN_HEIGHT, background_image.get_height()):
                screen.blit(background_image, (x, y))

        keys = pygame.key.get_pressed()
        moving_right = keys[pygame.K_RIGHT]
        if keys[pygame.K_SPACE] and player.on_ground:
            player.jump(jump_strength)

        player.apply_gravity(gravity)

        if player.rect.top > SCREEN_HEIGHT:
            reset_game()

        scroll_offset = speed if moving_right else 0
        platform_manager.update_platforms(scroll_offset)

        player.on_ground = False
        for plat in platform_manager.platforms:
            if player.collide_with_platform(plat):
                break

        if platform_manager.goal and player.rect.colliderect(platform_manager.goal):
            print("Čestitamo! Stigli ste do cilja!")
            running = False

        player.draw(screen)
        platform_manager.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()