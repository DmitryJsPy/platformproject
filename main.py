import pygame
import random
import sys

pygame.init()
clock = pygame.time.Clock()
fps = 75

# Загрузка музыки
music_win = pygame.mixer.Sound('music/molodec.mp3')
music_win.set_volume(0.2)
music_lose = pygame.mixer.Sound('music/lose.wav')
music_lose.set_volume(0.2)

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
bg = pygame.transform.scale(pygame.image.load('images/bg.jpg'), (1100, 900))
bg_width, bg_height = bg.get_size()

pygame.display.set_caption("Платформер")

y_speed = 0
gravity = 0.5
jump_strength = -10
on_ground = True

platforms = [
    (0, bg_height - 10, bg_width, 10),   
    (0, 850, 200, 10),     
    (200, 750, 100, 10),   
    (100, 650, 150, 10),    
    (300, 550, 200, 10),   
    (150, 450, 150, 10),   
    (400, 350, 200, 10),   
    (300, 250, 100, 10),   
    (100, 150, 100, 10),   
    (500, 500, 10, 300),   
    (600, 400, 200, 10),   
    (800, 300, 10, 100),   
]

camera = pygame.Rect(0, 0, screen_width, screen_height)
camera_step = 0.05

player = pygame.transform.scale(pygame.image.load('images/cat.png'), (70, 70))
player_rect = player.get_rect()
player_rect.x = 1000
player_rect.y = 850

pizza = pygame.transform.scale(pygame.image.load('images/pizza.png'), (70, 70))
pizza_rect = pizza.get_rect()
pizza_rect.x = 830
pizza_rect.y = 230

mouse_image = pygame.transform.scale(pygame.image.load('images/mouse.png'), (50, 50))
mouse_list = []
mouse_spawn_time = 0
max_mouse = 5

win_font = pygame.font.SysFont('font/font.ttf', 50)
win_text = win_font.render("МОЛОДЕЦ!!!", True, (0, 255, 0))

lose_font = pygame.font.SysFont('font/font.ttf', 50)
lose_text = lose_font.render("НЕМОЛОДЕЦ!!!", True, (0, 255, 0))

scale_factor = 1
scaling_up = True

button_width, button_height = 350, 70
restart_button = pygame.Rect((screen_width - button_width) // 2, screen_height // 2 + 80, button_width, button_height)
quit_button = pygame.Rect((screen_width - button_width) // 2, screen_height // 2 + 180, button_width, button_height)

restart_text = pygame.font.Font('font/font.ttf', 30).render('Начать заново!', True, (255, 255, 255))
quit_text = pygame.font.Font('font/font.ttf', 30).render('Выход', True, (255, 255, 255))


running = True
finish = False
facing_left = True
won = False

while running:
    clock.tick(fps)
    screen.blit(bg, (-camera.x, -camera.y))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if finish:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    finish = False
                    won = False
                    player_rect.x = 1000
                    player_rect.y = 850
                    mouse_list.clear()
                if quit_button.collidepoint(event.pos):
                    running = False

    if not finish:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            player_rect.x -= 3
            if not facing_left:
                player = pygame.transform.flip(player, True, False)
                facing_left = True

        if keys[pygame.K_d]:
            player_rect.x += 3
            if facing_left:
                player = pygame.transform.flip(player, True, False)
                facing_left = False

        if keys[pygame.K_SPACE] and on_ground:
            y_speed = jump_strength

        y_speed += gravity
        player_rect.y += y_speed

        if y_speed != 0:
            on_ground = False

        camera.x += (player_rect.x - screen_width // 2 - camera.x) * camera_step
        camera.y += (player_rect.y - screen_height // 2 - camera.y) * camera_step

        camera.x = max(0, min(camera.x, bg_width - screen_width))
        camera.y = max(0, min(camera.y, bg_height - screen_height))

        screen.blit(player, (player_rect.x - camera.x, player_rect.y - camera.y))
        screen.blit(pizza, (pizza_rect.x - camera.x, pizza_rect.y - camera.y))

        for platform in platforms:
            platform_rect = pygame.Rect(platform)
            if player_rect.colliderect(platform_rect) and y_speed > 0:
                player_rect.y = platform_rect.top - player_rect.height
                y_speed = 0
                on_ground = True

        if player_rect.colliderect(pizza_rect):
            if not finish:  
                music_win.play()  
            finish = True
            won = True

        if len(mouse_list) < max_mouse:
            if pygame.time.get_ticks() - mouse_spawn_time > 1000:
                mouse_rect = mouse_image.get_rect()
                mouse_rect.x = random.randint(0, screen_width - 50)
                mouse_rect.y = -50
                mouse_list.append(mouse_rect)
                mouse_spawn_time = pygame.time.get_ticks()

        for mouser_rect in mouse_list:
            mouser_rect.y += 2
            if mouser_rect.y > screen_height + 400:
                mouse_list.remove(mouser_rect)
            if player_rect.colliderect(mouser_rect):
                music_lose.play()
                finish = True
        for mouse_rect in mouse_list:
            screen.blit(mouse_image, (mouse_rect.x - camera.x, mouse_rect.y - camera.y))

        for platform in platforms:
            pygame.draw.rect(screen, (0, 100, 200), (platform[0] - camera.x, platform[1] - camera.y, platform[2], platform[3]))

    if finish:
        if scaling_up:
            scale_factor += 0.03
            if scale_factor >= 2:
                scaling_up = False
        else:
            scale_factor -= 0.03
            if scale_factor <= 1:
                scaling_up = True
        if won:
            scaled_text = pygame.transform.scale(win_text, (int(win_text.get_width() * scale_factor), int(win_text.get_height() * scale_factor)))
            
            scaled_text_rect = scaled_text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(scaled_text, scaled_text_rect)
        else:
            scaled_text = pygame.transform.scale(lose_text, (int(lose_text.get_width() * scale_factor), int(lose_text.get_height() * scale_factor)))
            
            scaled_text_rect = scaled_text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(scaled_text, scaled_text_rect)
        pygame.draw.rect(screen, (0, 100, 200), restart_button)
        pygame.draw.rect(screen, (0, 100, 200), quit_button)
        screen.blit(restart_text, (restart_button.x + (button_width - restart_text.get_width()) // 2, restart_button.y + (button_height - restart_text.get_height()) // 2))
        screen.blit(quit_text, (quit_button.x + (button_width - quit_text.get_width()) // 2, quit_button.y + (button_height - quit_text.get_height()) // 2))


    pygame.display.update()

pygame.quit()
sys.exit()
