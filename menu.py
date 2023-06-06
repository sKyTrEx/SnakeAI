import pygame
import sys

# Initialisiere Pygame
#pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

# Abrufen der Bildschirmauflösung
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Berechnen der Skalierungsfaktoren
scale_x = screen_width / (WINDOW_WIDTH * 1)
scale_y = screen_height / (WINDOW_HEIGHT * 1)

scale = min(scale_x, scale_y)

# Skalieren des Fensters
window_width_scaled = int(WINDOW_WIDTH * scale)
window_height_scaled = int(WINDOW_HEIGHT * scale)
screen = pygame.display.set_mode((window_width_scaled, window_height_scaled))
# Berechne die Schriftgröße basierend auf der Fensterhöhe
font_size = int(window_height_scaled / 40)



# Definiere die Hintergrundfarbe und die Schriftart
background_color = (50, 50, 50)
text_color = (255, 255, 255)
selected_color = (255, 0, 0)
font = pygame.font.SysFont('Arial', font_size)

# Definiere die Menüpunkte
menu_items = ['Spielen', 'KI spielen', 'Verlassen']
selected_item = 0
try:
    with open('scores.txt', 'r') as f:
        pass
except FileNotFoundError:
        with open('scores.txt', 'w') as f:
          
          f.write(f"0\t0000-00-00 00:00:00\t0\n")
          f.write(f"0\t0000-00-00 00:00:00\t0\n")
          f.write(f"0\t0000-00-00 00:00:00\t0\n")
          f.write(f"0\t0000-00-00 00:00:00\t0\n")
          f.write(f"0\t0000-00-00 00:00:00\t0\n")
          f.write(f"0\t0000-00-00 00:00:00\t0\n")
          f.write(f"0\t0000-00-00 00:00:00\t0\n")
          f.write(f"0\t0000-00-00 00:00:00\t0\n")
          f.write(f"0\t0000-00-00 00:00:00\t0\n")
          f.write(f"0\t0000-00-00 00:00:00\t0\n")
# Lese die Scores aus der scores.txt-Datei ein
scores = []
with open('scores.txt', 'r') as f:
    for line in f:
        score, date, counter = line.strip().split('\t')
        scores.append((int(score), date, int(counter)))

running = True
        
# Schleife zum Zeichnen des Menüs
while running:
    # Behandlung von Ereignissen
    for event in pygame.event.get():
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_item = (selected_item - 1) % len(menu_items)
            elif event.key == pygame.K_DOWN:
                selected_item = (selected_item + 1) % len(menu_items)
            elif event.key == pygame.K_RETURN:
                if selected_item == 0:
                    running = False
                    exec(open('game.py').read())
                    
                    #pygame.quit()
                    #sys.exit()
                elif selected_item == 1:
                    running = False
                    exec(open('ki.py').read())
                    #pygame.quit()
                    #sys.exit()
                elif selected_item == 2:
                    pygame.quit()
                    sys.exit()

    # Lösche den Bildschirm
    screen.fill(background_color)

    # Zeichne die Menüpunkte
    for i in range(len(menu_items)):
        text = font.render(menu_items[i], True, text_color)
        rect = text.get_rect()
        rect.left = font_size
        rect.top = i * font_size + font_size
        if i == selected_item:
            text = font.render(menu_items[i], True, selected_color)
        screen.blit(text, rect)

    # Zeichne die Scores
    score_text = font.render('Scores:', True, text_color)
    score_rect = score_text.get_rect()
    score_rect.left = window_width_scaled // 1.5
    score_rect.top = font_size
    screen.blit(score_text, score_rect)

    for i in range(len(scores)):
        score, date, counter = scores[i]
        text = font.render(f'{score} - {date} - {counter}', True, text_color)
        rect = text.get_rect()
        rect.left = window_width_scaled // 1.5
        rect.top = i * font_size + font_size  * 2
        screen.blit(text, rect)

    # Aktualisiere den Bildschirm
    pygame.display.flip()
