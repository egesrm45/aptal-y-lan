import pygame
import sys
import os
import configparser
import random
from settings import *
from utils import render_text, show_player_list
import eye_utils
import mouth_utils

pygame.init()

icon_path = os.path.join(os.path.dirname(__file__), 'gameicon.ico')
icon = pygame.image.load(icon_path)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('aptal yılan')
pygame.display.set_icon(icon)  # Set the loaded icon

class Snake:
    def __init__(self):
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = pygame.K_RIGHT
        self.new_block = False
        self.speed = 10
        self.move_delay = 150
        self.last_move_time = pygame.time.get_ticks()

    def move(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.move_delay:
            head_x, head_y = self.body[0]
            if self.direction == pygame.K_UP:
                new_head = (head_x, head_y - 20)
            elif self.direction == pygame.K_DOWN:
                new_head = (head_x, head_y + 20)
            elif self.direction == pygame.K_LEFT:
                new_head = (head_x - 20, head_y)
            elif self.direction == pygame.K_RIGHT:
                new_head = (head_x + 20, head_y)

            if (new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or
                new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT or
                new_head in self.body[1:]):
                return True  # Oyun bitti

            self.body = [new_head] + self.body[:-1]
            self.last_move_time = current_time
        return False

    def grow(self):
        self.body.append(self.body[-1])

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], 20, 20))
        eye1_center = (self.body[0][0] + 15, self.body[0][1] + 5)
        eye2_center = (self.body[0][0] + 15, self.body[0][1] + 15)
        eye_utils.draw_eye(screen, eye1_center, 10, 3, pygame.mouse.get_pos())
        eye_utils.draw_eye(screen, eye2_center, 10, 3, pygame.mouse.get_pos())

    def check_collision(self, food):
        if self.body[0] == food.position:
            return True
        return False

    def change_direction(self, new_direction):
        if (new_direction == pygame.K_UP and self.direction != pygame.K_DOWN) or \
           (new_direction == pygame.K_DOWN and self.direction != pygame.K_UP) or \
           (new_direction == pygame.K_LEFT and self.direction != pygame.K_RIGHT) or \
           (new_direction == pygame.K_RIGHT and self.direction != pygame.K_LEFT):
            self.direction = new_direction

class Food:
    def __init__(self):
        self.position = (random.randint(0, SCREEN_WIDTH // 20 - 1) * 20,
                         random.randint(0, SCREEN_HEIGHT // 20 - 1) * 20)
        self.color = RED if random.choice([True, False]) else BLUE
        self.speed_effect = -2 if self.color == RED else 2

    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.position[0], self.position[1], 20, 20))

def show_game_over_screen(screen, score):
    screen.fill(BLACK)
    
    font = pygame.font.Font(None, 74)
    text = font.render("OYUN BİTTİ", True, RED)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 3 - text.get_height() // 2))
    
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(f"SKOR: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    
    retry_font = pygame.font.Font(None, 24)
    retry_text = retry_font.render("TEKRAR OYNAMAK ICIN 'ENTER'", True, WHITE)
    screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, SCREEN_HEIGHT * 3 // 4))
    
    face_center_y = SCREEN_HEIGHT * 1 // 8
    eye1_center = (SCREEN_WIDTH // 2 - 50, face_center_y - 30)
    eye2_center = (SCREEN_WIDTH // 2 + 50, face_center_y - 30)
    eye_utils.draw_eye(screen, eye1_center, 30, 10, (SCREEN_WIDTH // 2, face_center_y + 50))
    eye_utils.draw_eye(screen, eye2_center, 30, 10, (SCREEN_WIDTH // 2, face_center_y + 50))
    
    pygame.display.flip()

def show_settings(screen):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    message = "Ege SÜRÜM Tarafından oluşturuldu."
    text_surface = font.render(message, True, WHITE)
    screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()

def main():
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    show_menu = True
    in_game = False
    in_settings = False
    is_online = False
    clock = pygame.time.Clock()

    menu_options = ["1. OYNA", "2. AYARLAR", "3. MENÜYE DÖN", "4. ÇIKIŞ"]
    selected_option = 0
    
    current_player = ""

    input_box = pygame.Rect((SCREEN_WIDTH // 2) - 100, (SCREEN_HEIGHT // 2) - 16, 200, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = BLUE
    color = color_inactive
    active = False
    text = ''
    done = False
    delete_key_held = False
    delete_key_timer = 0
    delete_key_start_time = 0
    delete_key_delay = 500
    delete_key_interval = 50
    delete_hold_threshold = 3000
    
    show_message = True
    message_timer = 0
    message_duration = 10000

    menu_rects = []

    snake = Snake()
    food = Food()
    score = 0
    score_font = pygame.font.Font(None, 36)

    while not done:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if in_game or in_settings:
                        show_menu = True
                        in_game = False
                        in_settings = False
                    else:
                        pygame.quit()
                        sys.exit()
                elif event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT] and in_game:
                    snake.change_direction(event.key)
                elif event.key == pygame.K_RETURN:
                    if current_player == "":
                        active = not active
                    else:
                        if selected_option == 0:
                            print(f"oyna, {current_player}")
                            show_menu = False
                            in_game = True
                            player_file_path = f'characters/character_details/{current_player}.txt'
                            print(f"oyuncunun dosyası: {player_file_path}")
                            if not os.path.exists('characters/character_details'):
                                os.makedirs('characters/character_details')
                            with open(player_file_path, 'w') as file:
                                file.write(f"OYUNCU: {current_player}\n")
                                file.write("SEVIYE: 1\n")
                            is_online = True
                        elif selected_option == 1:
                            print("AYARLAR")
                            show_menu = False
                            in_settings = True
                            is_online = False
                        elif selected_option == 2:
                            print("MENÜ")
                            show_menu = True
                            in_game = False
                            is_online = False
                        elif selected_option == 3:
                            pygame.quit()
                            sys.exit()
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_3:
                    if in_settings:
                        show_menu = True
                        in_settings = False
                    else:
                        print("MENÜ")
                        show_menu = True
                        in_game = False
                        is_online = False
                elif active:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif len(text) < 15 and (event.unicode.isalpha() or event.unicode in 'çÇğĞıİöÖşŞüÜ'):
                        text += event.unicode
            #elif event.type == pygame.KEYUP:
                #if event.key == pygame.K_TAB:
                   # show_player_list_flag = False
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    delete_key_held = False
                    if current_time - delete_key_start_time >= delete_hold_threshold:
                        text = ''
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
                
                if show_menu:
                    for i, rect in enumerate(menu_rects):
                        if rect.collidepoint(event.pos):
                            selected_option = i
                            if current_player != "":
                                if selected_option == 0:
                                    print(f"OYNA {current_player}")
                                    show_menu = False
                                    in_game = True
                                elif selected_option == 1:
                                    print("AYARLAR")
                                    show_menu = False
                                    in_settings = True
                                elif selected_option == 2:
                                    print("MENÜ")
                                    show_menu = True
                                    in_game = False
                                elif selected_option == 3:
                                    pygame.quit()
                                    sys.exit()
                            break

        screen.fill(BLACK)

        if current_player == "":
            render_text(screen, "İSİM GİR:", small_font, WHITE, (input_box.x, input_box.y - 30))
            txt_surface = small_font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, color, input_box, 2)

            eye1_center = (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100)
            eye2_center = (SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 - 100)
            eye_utils.draw_eye(screen, eye1_center, 30, 10, pygame.mouse.get_pos())
            eye_utils.draw_eye(screen, eye2_center, 30, 10, pygame.mouse.get_pos())

            if active and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if text.strip().isalpha() and 10 <= len(text.strip()) <= 15:
                    current_player = text.strip()
                    player_file_path = f'characters/character_details/{current_player}.txt'
                    if os.path.exists(player_file_path):
                        with open(player_file_path, 'r') as file:
                            print(file.read())
                    else:
                        with open(player_file_path, 'w') as file:
                            file.write(f"OYUNCU: {current_player}\n")
                            file.write("SEVIYE: 1\n")
                    show_menu = True
                    active = False
                else:
                    print("Hata: Oyuncu adı alfabetik olmalı ve 10 ila 15 karakter arasında olmalıdır")

        else:
            menu_rects = []
            #if show_player_list_flag:
             #   show_player_list(screen, current_player)
            if show_menu:
                for i, option in enumerate(menu_options):
                    color = YELLOW if i == selected_option else WHITE
                    text_surface = font.render(option, True, color)
                    screen.blit(text_surface, (20, 20 + i * 40))
                    text_rect = text_surface.get_rect(topleft=(20, 20 + i * 40))
                    menu_rects.append(text_rect)
            elif in_game:
                game_over = snake.move()

                if game_over:
                    show_game_over_screen(screen, score)
                    waiting_for_restart = True
                    while waiting_for_restart:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                    snake = Snake()
                                    food = Food()
                                    score = 0
                                    waiting_for_restart = False
                                elif event.key == pygame.K_3:
                                    show_menu = True
                                    in_game = False
                                    is_online = False
                                    waiting_for_restart = False
                else:
                    if snake.check_collision(food):
                        snake.grow()
                        snake.speed += food.speed_effect
                        food = Food()
                        score += 1

                    snake.draw()
                    food.draw()

                    score_text = score_font.render(f"SKOR: {score}", True, WHITE)
                    screen.blit(score_text, (10, 10))
            elif in_settings:
                show_settings(screen)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    show_menu = True
                    in_settings = False
                    is_online = False

        status_text = "Çevrimiçi" if is_online else "Çevrimdışı"
        status_surface = font.render(status_text, True, WHITE)
        screen.blit(status_surface, (SCREEN_WIDTH - 100, 10))

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
