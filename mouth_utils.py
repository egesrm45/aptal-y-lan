import pygame

def draw_mouth(screen, mouth_center, width, height):

    rect = pygame.Rect(mouth_center[0] - width // 2, mouth_center[1] - height // 2, width, height)
    pygame.draw.arc(screen, (255, 0, 0), rect, 0, 3.14, 5)
