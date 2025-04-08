import pygame
from sys import exit
from random import randint
import os
import sys
import asyncio

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Kerriberry Game")

async def main():
    # Add these global variables at the start of main()
    global player_index, player_surf, player_walk, player_jump
    player_index = 0

    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            # Get the directory where the script is located
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)


    def display_score():
        current_time = int(pygame.time.get_ticks() / 1000) - start_time
        score_surf = Pixel_font.render(f'Adventure Score: {current_time}', True, 'Hot Pink')
        score_rect = score_surf.get_rect(center=(400, 100))
        screen.blit(score_surf, score_rect)
        return current_time


    def obstacle_movement(obstacle_list, current_time):
        if obstacle_list:
            base_speed = 5
            speed_increment = current_time * 0.2
            for obstacle_rect in obstacle_list:
                obstacle_rect.x -= base_speed + speed_increment
                if obstacle_rect.bottom == 300:
                    screen.blit(frog_surf, obstacle_rect)
                else:
                    screen.blit(bird_surf, obstacle_rect)

            # Remove obstacles that move off-screen
            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
            return obstacle_list
        else:
            return []


    def collisions(player, obstacles):
        if obstacles:
            for obstacle_rect in obstacles:
                if player.colliderect(obstacle_rect): return False
        return True


    def player_animation():
        global player_surf, player_index, player_walk, player_jump

        if player_rect.bottom < 300:
            player_surf = player_jump
        else:
            player_index += 0.1
            if player_index >= len(player_walk): player_index = 0
            player_surf = player_walk[int(player_index)]


    pygame.mixer.pre_init(44100, -16, 2, 512)  # Add this line before pygame.init()
    pygame.init()

    # Add after pygame.init() but before loading resources
    def show_loading_screen():
        screen = pygame.display.set_mode((800, 400))
        screen.fill((94, 129, 162))
        loading_font = pygame.font.Font(None, 40)
        loading_text = loading_font.render("Loading...", True, "white")
        loading_rect = loading_text.get_rect(center=(400, 200))
        screen.blit(loading_text, loading_rect)
        pygame.display.update()

    # Add this right after pygame.init()
    show_loading_screen()

    # Main Variables
    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption('Kerri Berry Princess Fairy')
    clock = pygame.time.Clock()
    Karris_font_big = pygame.font.Font(resource_path('graphics/Fonts/Kerrisfont.ttf'), 60)
    Karris_font_little = pygame.font.Font(resource_path('graphics/Fonts/Kerrisfont.ttf'), 30)
    Pixel_font = pygame.font.Font(resource_path('graphics/Fonts/Pixeltype.ttf'), 40)
    game_active = False
    start_time = 0
    score = 0
    jump_sound = pygame.mixer.Sound(resource_path('audio/Jump.ogg'))
    jump_sound.set_volume(0.5)
    Music = pygame.mixer.Sound(resource_path('audio/Music.ogg'))
    Music.set_volume(0.5)
    bgmusic = pygame.mixer.Sound(resource_path('audio/bgmusic.ogg'))

    obstacle_rect_list = []

    # In Game Stuff
    background_surface = pygame.image.load(resource_path('graphics/background.png')).convert()
    ground_surface = pygame.image.load(resource_path('graphics/ground.png')).convert()

    title_surf = Karris_font_big.render("Kerri's adventure!", True, 'hot pink')
    title_rect = title_surf.get_rect(center=(400, 50))

    little_title_surf = Pixel_font.render("Wt. Karri Berry Princess Fairy", False, 'hot pink')
    little_title_rect = title_surf.get_rect(center=(450, 120))

    bird_frame1 = pygame.image.load(resource_path('graphics/bird/bird1.png')).convert_alpha()
    bird_frame2 = pygame.image.load(resource_path('graphics/bird/bird2.png')).convert_alpha()
    bird_frames = [bird_frame1, bird_frame2]
    bird_frame_index = 0
    bird_surf = bird_frames[bird_frame_index]

    frog_frame1 = pygame.image.load(resource_path('graphics/frog/frog.png')).convert_alpha()
    frog_frame2 = pygame.image.load(resource_path('graphics/frog/frog1.png')).convert_alpha()
    frog_frames = [frog_frame1, frog_frame2]
    frog_frame_index = 0
    frog_surf = frog_frames[frog_frame_index]

    player_walk_1 = pygame.image.load(resource_path('graphics/Player/kerri.png')).convert_alpha()
    player_walk_2 = pygame.image.load(resource_path('graphics/Player/kerriwalk.png')).convert_alpha()
    player_walk = [player_walk_1, player_walk_2]
    player_index = 0
    player_jump = pygame.image.load(resource_path('graphics/Player/kerrijump.png')).convert_alpha()
    player_surf = player_walk[player_index]
    player_rect = player_surf.get_rect(midbottom=(80, 300))
    player_gravity = 0

    # Title Screen Variables
    player_stand = pygame.image.load(resource_path('graphics/player/Kerrijump.png')).convert_alpha()
    player_stand = pygame.transform.scale2x(player_stand)
    player_stand_rect = player_stand.get_rect(center=(400, 200))

    begin_title = Pixel_font.render("Press Space to Explore!", True, (64, 64, 64))
    begin_title_rect = begin_title.get_rect(center=(400, 350))

    # Timer
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, 1500)

    bird_animation_timer = pygame.USEREVENT + 3
    pygame.time.set_timer(bird_animation_timer, 500)

    frog_animation_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(frog_animation_timer, 500)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if game_active:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                        player_gravity = -20

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                        player_gravity = -20
                        jump_sound.play()

            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)

            if game_active:
                if event.type == obstacle_timer:
                    if randint(0, 2):
                        obstacle_rect_list.append(frog_surf.get_rect(bottomright=(randint(900, 1100), 300)))
                    else:
                        obstacle_rect_list.append(bird_surf.get_rect(bottomright=(randint(900, 1100), 210)))

                if event.type == frog_animation_timer:
                    if frog_frame_index == 0:
                        frog_frame_index = 1
                    else:
                        frog_frame_index = 0
                    frog_surf = frog_frames[frog_frame_index]

                if event.type == bird_animation_timer:
                    if bird_frame_index == 0:
                        bird_frame_index = 1
                    else:
                        bird_frame_index = 0
                    bird_surf = bird_frames[bird_frame_index]

        if game_active:
            Music.stop()
            bgmusic.play(loops=-1)
            screen.blit(background_surface, (0, 0))
            screen.blit(ground_surface, (0, 300))
            score = display_score()

            # player
            player_gravity += 1
            player_rect.y += player_gravity
            if player_rect.bottom >= 300:
                player_rect.bottom = 300
            player_animation()
            screen.blit(player_surf, player_rect)

            # Obstacle movement
            obstacle_rect_list = obstacle_movement(obstacle_rect_list, score)

            # collisions
            game_active = collisions(player_rect, obstacle_rect_list)


        else:
            bgmusic.stop()
            Music.play(loops=-1)
            screen.fill((94, 129, 162))
            screen.blit(title_surf, title_rect)
            screen.blit(little_title_surf, little_title_rect)
            screen.blit(player_stand, player_stand_rect)
            obstacle_rect_list.clear()
            player_rect.midbottom = (80, 300)
            player_gravity = 0

            score_message = Pixel_font.render(f'Adventure Score: {score}', True, 'Hot Pink')
            score_message_rect = score_message.get_rect(center=(400, 350))

            if score == 0:
                screen.blit(begin_title, begin_title_rect)
            else:
                screen.blit(score_message, score_message_rect)

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
