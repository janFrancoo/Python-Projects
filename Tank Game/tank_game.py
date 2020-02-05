import math
import pygame
import random

pygame.init()
black = (0, 0, 0)
white = (200, 200, 200)
red = (186, 0, 0)
green = (0, 186, 0)
dark_green = (0, 130, 0)
blue = (0, 0, 186)
small_font = pygame.font.SysFont("comicsansms", 25)
med_font = pygame.font.SysFont("comicsansms", 50)
large_font = pygame.font.SysFont("comicsansms", 80)

width = 800
height = 600
clock = pygame.time.Clock()
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tanks')
explosion_sound = pygame.mixer.Sound("explosion.wav")
# pygame.display.set_icon(apple_img)


def button(text, c, x, y, w, h):
    active_c = (c[0] + 40, c[1] + 40, c[2] + 40)
    mouse_pos = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()
    if x + h > mouse_pos[0] > x and y + w > mouse_pos[1] > y:
        pygame.draw.rect(game_display, active_c, (x, y, h, w))
        if clicked[0] == 1:
            return 1
    else:
        pygame.draw.rect(game_display, c, (x, y, h, w))
    msg_to_screen(text, [x + 20, y + 5], (255, 255, 255), small_font)
    return 0


def check_intersection(x1, y1, x2, y2, block_size):
    if ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1/2) < block_size:
        return True
    return False


def msg_to_screen(msg, pos, color, font):
    screen_text = font.render(msg, True, color)
    game_display.blit(screen_text, pos)


def polar_to_cartesian(origin_x, origin_y, r, angle):
    angle = math.radians(angle)
    x = r * math.cos(angle) + origin_x
    y = r * math.sin(angle) + origin_y
    return int(x), int(y)


def tank(x, y, w, h, r, angle, color):
    circle_x, circle_y = (x + w // 2), y
    weapon_end_point_x, weapon_end_point_y = polar_to_cartesian(circle_x, circle_y, r, angle)
    pygame.draw.rect(game_display, color, (x, y, w, h))
    pygame.draw.circle(game_display, color, (circle_x, circle_y), int(w * 0.3))
    pygame.draw.line(game_display, color, (circle_x, circle_y), (weapon_end_point_x, weapon_end_point_y), 4)
    wheel_x, wheel_y, wheel_count = x + 5, y + h, (w // 5) - 1
    for i in range(wheel_count):
        pygame.draw.circle(game_display, color, (wheel_x, wheel_y), 3)
        wheel_x += 5
    return weapon_end_point_x, weapon_end_point_y, angle


def draw_health(health_value, tank_type):
    if tank_type == "enemy":
        game_display.fill(green, rect=[10, 20, int(health_value * 1.5), 20])
        msg_to_screen(str(health_value), (170, 10), red, small_font)
    if tank_type == "player":
        game_display.fill(green, rect=[790 - int(health_value * 1.5), 20, int(health_value * 1.5), 20])
        msg_to_screen(str(health_value), (590, 10), black, small_font)


def fire(x, y, angle, speed, gravity):
    e_x, e_y = polar_to_cartesian(x, y, speed, angle)
    dx, dy = e_x - x, e_y - y
    x += dx
    y += (dy - gravity)
    pygame.draw.circle(game_display, dark_green, (x, y), 5)
    if 0 < x < width and 0 < y < height:
        return x, y, True, gravity
    else:
        return x, y, False, gravity


def start_screen():
    to_game = False
    while not to_game:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key != pygame.K_q:
                    to_game = True
                else:
                    quit()

        game_display.fill(white)
        msg_to_screen("Welcome to the tanks!", [(width // 2) - 200, (height // 2) - 50], red,
                      small_font)
        if button("Play", red, (width // 3 - 100), 400, 50, 100) == 1:
            break
        if button("Quit", green, (width // 2 - 100), 400, 50, 100):
            pygame.quit()
            quit()
        pygame.display.update()


def pause_screen():
    to_game = False
    while not to_game:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit()
                if event.key == pygame.K_p:
                    to_game = True

        game_display.fill(white)
        msg_to_screen("Press P again to go back or press Q to exit", [(width // 2) - 200, (height // 2) - 50],
                      blue, small_font)
        pygame.display.update()


def game_loop():
    x, y, dx, dy, t_width, t_height, r, angle, health = width - 100, height - 100, 0, 0, 80, 40, 60, 200, 100
    is_fired, game_over, game_exit = False, False, False
    fire_x, fire_y, fire_angle, fire_speed, g_force = 0, 0, 0, 22, 1
    barrier_width, barrier_height = 10 + int(random.random() * 100) % 90, 200 + int(random.random() * 100)
    barrier_x, barrier_y = 300 + (int(random.random() * 1000) % (width - 600)), height - barrier_height
    enemy_x, enemy_y, enemy_angle, enemy_health = 20, y, 315, 100

    while not game_exit:
        game_display.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause_screen()
                if event.key == pygame.K_LEFT:
                    dx = -5
                if event.key == pygame.K_RIGHT:
                    dx = 5
                if event.key == pygame.K_UP:
                    if 180 <= angle + 5 <= 270:
                        angle += 5
                if event.key == pygame.K_DOWN:
                    if 180 <= angle - 5 <= 270:
                        angle -= 5
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    if not is_fired:
                        is_fired = True
                        g_force = 1
                        fire_x, fire_y, fire_angle = tank(x, y, t_width, t_height, r, angle, black)
                if event.key == pygame.K_SPACE:
                    dx = 0
                if event.key == pygame.K_r:
                    game_loop()

        tank(x, y, t_width, t_height, r, angle, black)
        draw_health(health, "player")
        tank(enemy_x, enemy_y, t_width, t_height, r, enemy_angle, red)
        draw_health(enemy_health, "enemy")
        pygame.draw.rect(game_display, black, (barrier_x, barrier_y, barrier_width, barrier_height))
        pygame.draw.rect(game_display, green, (0, y + t_height + 3, width, 60))

        if barrier_x + barrier_width < x + dx < width - t_width:
            x += dx
        if is_fired:
            fire_x, fire_y, is_fired, g_force = fire(fire_x, fire_y, fire_angle, fire_speed, g_force)
            g_force -= 1
        if barrier_x < fire_x < barrier_x + barrier_width and barrier_y < fire_y < barrier_y + height:
            is_fired = False
        if enemy_x <= fire_x <= enemy_x + t_width and enemy_y <= fire_y <= enemy_y + t_height:
            if is_fired:
                enemy_health -= 5
                pygame.mixer.Sound.play(explosion_sound)
            is_fired = False

        pygame.display.update()
        clock.tick(30)

        while game_over:
            game_display.fill(white)
            msg_to_screen("Game Over", [(width // 2) - 25, 200], red, small_font)
            msg_to_screen("Press C to play again or Q to exit", [(width // 2) - 100, 300], black, small_font)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit, game_over = True, False
                    if event.key == pygame.K_c:
                        pass

    pygame.quit()
    quit()


start_screen()
game_loop()
