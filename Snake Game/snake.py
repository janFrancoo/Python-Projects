import time
import pygame
import random

pygame.init()
black = (0, 0, 0)
white = (200, 200, 200)
red = (186, 0, 0)
some_stupid_color = (158, 55, 94)
some_stupid_color_2 = (38, 35, 194)
small_font = pygame.font.SysFont("comicsansms", 25)
med_font = pygame.font.SysFont("comicsansms", 50)
large_font = pygame.font.SysFont("comicsansms", 80)

width = 800
height = 600
clock = pygame.time.Clock()
img = pygame.image.load('head.png')
apple_img = pygame.image.load('apple.png')
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('MyFirstGame')
pygame.display.set_icon(apple_img)


def check_intersection(x1, y1, x2, y2, block_size):
    if ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1/2) < block_size:
        return True
    return False


def snake(head_img, snake_list, block_size):
    g = 150
    head = (int(snake_list[-1][0]), int(snake_list[-1][1]))
    game_display.blit(head_img, head)
    for x, y in snake_list:
        if (x, y) != head:
            game_display.fill((0, g, 0), rect=[int(x), int(y), block_size, block_size])
        g = (g + 5) % 255


def msg_to_screen(msg, pos, color, font):
    screen_text = font.render(msg, True, color)
    game_display.blit(screen_text, pos)


def change_head(head_img, snake_dir):
    if snake_dir == "left":
        head_img = pygame.transform.rotate(head_img, 90)
    elif snake_dir == "right":
        head_img = pygame.transform.rotate(head_img, -90)
    elif snake_dir == "down":
        head_img = pygame.transform.rotate(head_img, 180)
    else:
        head_img = img
    return head_img


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
        msg_to_screen("Welcome to my first pyGame game!", [(width // 2) - 200, (height // 2) - 50], some_stupid_color,
                      small_font)
        msg_to_screen("Press Q for exit or press any other key to start!", [(width // 2) - 300, (height // 2) + 50],
                      some_stupid_color_2, small_font)
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
                      some_stupid_color_2, small_font)
        pygame.display.update()


def game_loop():
    direction, eat_time = "", 0
    x, y, dx, dy, s, block_size, score, game_exit, game_over = 300, 300, 0, 0, 10.0, 15, 0, False, False
    apple_x = round(random.randrange(0, width - block_size) / s) * s
    apple_y = round(random.randrange(0, height - block_size) / s) * s
    snake_list, snake_len = [], 1

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx != s:
                    dx, dy, direction = -s, 0, "left"
                if event.key == pygame.K_RIGHT and dx != -s:
                    dx, dy, direction = s, 0, "right"
                if event.key == pygame.K_UP and dy != s:
                    dx, dy, direction = 0, -s, "up"
                if event.key == pygame.K_DOWN and dy != -s:
                    dx, dy, direction = 0, s, "down"
                if event.key == pygame.K_p:
                    pause_screen()

        if x >= width - block_size:
            x = 0
        if x < 0:
            x = (width - block_size)
        if y >= height - block_size:
            y = 0
        if y < 0:
            y = height - block_size

        x += dx
        y += dy

        if check_intersection(x, y, apple_x, apple_y, block_size):
            t = time.perf_counter()
            if eat_time != 0 and abs(eat_time - t) < 1:
                score += 1
                snake_len += 1
            eat_time = t
            apple_x = round(random.randrange(0, width - block_size) / s) * s
            apple_y = round(random.randrange(0, height - block_size) / s) * s
            snake_len += 1
            score += 1

        game_display.fill(white)
        game_display.blit(apple_img, (int(apple_x), int(apple_y)))
        msg_to_screen("Score: {} - P for Pause".format(score), [10, 10], black, small_font)

        head = [x, y]
        snake_list.append(head)
        if len(snake_list) > snake_len:
            del snake_list[0]
        snake(change_head(img, direction), snake_list, block_size)

        for block in snake_list[:-1]:
            if block == head:
                game_over = True

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
                        x, y, dx, dy, game_over, snake_len, snake_list, score = 300, 300, 0, 0, False, 1, [], 0

    pygame.quit()
    quit()


start_screen()
game_loop()
