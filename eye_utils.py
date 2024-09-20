import pygame
import math

def draw_eye(screen, eye_center, eye_radius, pupil_radius, mouse_pos):

    pygame.draw.circle(screen, (255, 255, 255), eye_center, eye_radius)
    

    dx = mouse_pos[0] - eye_center[0]
    dy = mouse_pos[1] - eye_center[1]
    

    distance = math.hypot(dx, dy)
    

    max_distance = eye_radius - pupil_radius
    if distance > max_distance:
        dx = dx / distance * max_distance
        dy = dy / distance * max_distance
    

    pupil_center = (int(eye_center[0] + dx), int(eye_center[1] + dy))
    

    pygame.draw.circle(screen, (0, 0, 0), pupil_center, pupil_radius)
