import pygame
import random
import time
import datetime
import subprocess
import sys

# Initialisiere Pygame und setze Fenstergröße
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

# Setze Titel und Icon
pygame.display.set_caption("Snake")
icon = pygame.image.load('snake_icon.png')
pygame.display.set_icon(icon)

# Setze Hintergrundfarbe und FPS
bg_color = pygame.Color('grey12')
fps = pygame.time.Clock()


# Setze Snake-Startposition und -Geschwindigkeit
snake_head= [400, 300]
snake_body = [[400,300], [390,300], [380,300]]
snake_speed = pygame.math.Vector2(1, 0)

# Setze Futter-Startposition
food_pos = [random.randrange(1, (window_width_scaled // 20)) * 20, random.randrange(1, (window_height_scaled // 20)) * 20]
food_spawn = True

# Setze Richtungsvariablen
direction = 'RIGHT'
change_to = direction

# Setze Punkte
score = 0
counter = 0

# Setze variablen auf False
game_is_over = False
food_eaten = False

# Setze Schriftart und -farbe für Punktzahl
font = pygame.font.Font('freesansbold.ttf', 18)
score_font = pygame.font.Font('freesansbold.ttf', 28)
score_color = pygame.Color('white')

# Setze Game Over-Text
game_over_font = pygame.font.Font('freesansbold.ttf', 48)
game_over_color = pygame.Color('white')

def restart_game():
  global snake_head, snake_body, snake_speed, direction, change_to, score, food_pos, food_spawn, game_is_over
  snake_head = [400, 300]
  snake_body = [[400,300], [390,300], [380,300], [370,300], [360,300]]
  snake_speed = pygame.math.Vector2(1, 0)
  food_pos = [random.randrange(1, (window_width_scaled // 20)) * 20, random.randrange(1, (window_height_scaled // 20)) * 20]
  food_spawn = True
  direction = 'RIGHT'
  change_to = direction
  score = 0
  game_is_over = False

def game_over():
  # Lese die bisherigen Punktestände aus der Textdatei

  with open('scores.txt', 'r') as f:
    scores = []
    for line in f:
      s, _, _ = line.split('\t')
      scores.append(int(s))
  # Prüfe, ob der aktuelle Score ein neuer Highscore ist
  if score > max(scores):
    # Setze Schriftart und -farbe für den "Highscore"-Text
    font = pygame.font.Font('freesansbold.ttf', 48)
    color = pygame.Color('red')
    # Render den "Highscore"-Text
    highscore_text = font.render('Highscore', True, color)
    # Setze Schriftart und -farbe für den aktuellen Punktestand-Text
    font = pygame.font.Font('freesansbold.ttf', 28)
    color = pygame.Color('white')
    # Render den aktuellen Punktestand-Text
    score_text = font.render('Score: ' + str(score), True, color)
  else:
    # Setze Schriftart und -farbe für den "Game Over"-Text
    font = pygame.font.Font('freesansbold.ttf', 48)
    color = pygame.Color('white')
    # Render den "Game Over"-Text
    highscore_text = font.render('Game Over', True, color)
    # Setze Schriftart und -farbe für den aktuellen Punktestand-Text
    font = pygame.font.Font('freesansbold.ttf', 28)
    color = pygame.Color('white')
    # Render den aktuellen Punktestand-Text
    score_text = font.render('Score: ' + str(score), True, color)
  # Zeichne den "Highscore"-Text und den aktuellen Punktestand-Text auf den Bildschirm
  screen.blit(highscore_text, (window_width_scaled/3, window_height_scaled/3))
  screen.blit(score_text, (window_width_scaled/3, window_height_scaled/3 + 50))
  # Setze game_over auf True
  game_is_over = True
  pygame.display.update()
  time.sleep(2)
  # Rufe die Funktion auf, wenn das Spiel beendet wird
  save_score(score, counter)
  restart_game()
  game_is_over = False

"""try:
    with open('scores.txt', 'r') as f:
        pass
except FileNotFoundError:
        with open('scores.txt', 'w') as f:
          
          f.write(f"0\t0000-00-00 00:00:00 0\n")"""
def save_score(score, counter):
  # Lese die bisherigen Punktestände aus der Textdatei

  with open('scores.txt', 'r') as f:
    scores = []
    dates = []
    counters = []
    for line in f:
      s, d, c = line.split('\t')
      scores.append(int(s))
      dates.append(d.strip())
      counters.append(int(c))
  # Füge die aktuelle Punktzahl nur hinzu, wenn sie unter den 10 besten ist
  if len(scores) < 10 or score > min(scores):
    # Entferne den geringsten Score, wenn die Anzahl der Scores über 10 ist
    if len(scores) == 10:
      min_index = scores.index(min(scores))
      scores.pop(min_index)
      dates.pop(min_index)
      counters.pop(min_index)
    # Öffne die Textdatei zum Schreiben
    with open('scores.txt', 'w') as f:
      # Füge den aktuellen Score und das aktuelle Datum und die Uhrzeit hinzu
      scores.append(score)
      counters.append(counter)
      now = datetime.datetime.now()
      dates.append(now.strftime('%Y-%m-%d %H:%M:%S'))
      # Schreibe alle Scores und Datumsangaben in die Textdatei
      for s, d, c in zip(scores, dates, counters):
        f.write(f"{s}\t{d}\t{c}\n")


running = True
# Setze Hauptschleife
while True:
  for event in pygame.event.get():
     if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        runing = False
        exec(open('menu.py').read())
        #pygame.quit()
        #sys.exit(subprocess.call(["python", "run.py"]))
      if event.key == pygame.K_UP:
        change_to = 'UP'
      if event.key == pygame.K_DOWN:
        change_to = 'DOWN'
      if event.key == pygame.K_LEFT:
        change_to = 'LEFT'
      if event.key == pygame.K_RIGHT:
        change_to = 'RIGHT'


  # Überprüfe, ob Snake sich in die falsche Richtung bewegt
  if change_to == 'UP' and direction != 'DOWN':
    direction = 'UP'
  if change_to == 'DOWN' and direction != 'UP':
    direction = 'DOWN'
  if change_to == 'LEFT' and direction != 'RIGHT':
    direction = 'LEFT'
  if change_to == 'RIGHT' and direction != 'LEFT':
    direction = 'RIGHT'

  # Bewege Snake in aktuelle Richtung
  if direction == 'UP':
    snake_head[1] -= 10
  if direction == 'DOWN':
    snake_head[1] += 10
  if direction == 'LEFT':
    snake_head[0] -= 10
  if direction == 'RIGHT':
    snake_head[0] += 10

  # Füge neues Snake-Segment hinzu, falls Snake Futter gefressen hat
  snake_body.insert(0, list(snake_head))
  if snake_head[0] == food_pos[0] and snake_head[1] == food_pos[1]:
    score += 1
    food_eaten = True
    food_spawn = False
  else:
    snake_body.pop()
    
  if not food_spawn:
    food_pos = [random.randrange(1, (window_width_scaled // 20)) * 20, random.randrange(1, (window_height_scaled // 20)) * 20]
  food_spawn = True

  screen.fill(bg_color)

  # Zeichne Snake
  for i, pos in enumerate(snake_body):
      if i == 0:  # Wenn es sich um den Kopf handelt
          pygame.draw.rect(screen, pygame.Color('red'), pygame.Rect(pos[0], pos[1], 10, 10))
      else:  # Wenn es sich um den Körper handelt
          pygame.draw.rect(screen, pygame.Color('brown'), pygame.Rect(pos[0], pos[1], 10, 10))

  # Zeichne Futter
  pygame.draw.rect(screen, pygame.Color('green'), pygame.Rect(food_pos[0], food_pos[1], 10, 10))

  # Zeichne Punktzahl
  score_font = font.render('Score: ' + str(score), True, score_color)
  screen.blit(score_font, [0, 0])

  # Überprüfe, ob Snake sich selbst gebissen hat
  if snake_head[0] < 0 or snake_head[0] > window_width_scaled-10:
    game_over()
  if snake_head[1] < 0 or snake_head[1] > window_height_scaled-10:
    game_over()
    
  for block in snake_body[1:]:
    if snake_head[0] == block[0] and snake_head[1] == block[1]:
      game_over()

  

  pygame.display.update()
  fps.tick(20)



