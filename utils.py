import pygame
from settings import *

def render_text(screen, text, font, color, pos):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

def show_player_list(screen, current_player):
    font = pygame.font.Font(None, 24)
    y_offset = 20
    
    render_text(screen, f"{current_player} (You): online", font, GREEN, (20, y_offset))
    y_offset += 30

    for player, status in player_statuses.items():
        color = GREEN if status == "online" else RED
        render_text(screen, f"{player}: {status}", font, color, (20, y_offset))
        y_offset += 30
