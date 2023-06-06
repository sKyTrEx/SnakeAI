import pygame


# Initialisiere Pygame
pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

# Abrufen der Bildschirmauflösung
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Berechnen der Skalierungsfaktoren
scale_x = screen_width / (WINDOW_WIDTH * 1.1)
scale_y = screen_height / (WINDOW_HEIGHT * 1.1)

scale = min(scale_x, scale_y)

# Skalieren des Fensters
window_width_scaled = int(WINDOW_WIDTH * scale)
window_height_scaled = int(WINDOW_HEIGHT * scale)
screen = pygame.display.set_mode((window_width_scaled, window_height_scaled))

exec(open('menu.py').read())
#pygame.quit()