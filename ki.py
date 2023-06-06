import datetime
import json
import math
import numpy as np
import pygame
import random
import sys
import time
import subprocess

from typing import List


class State:
    one_eighth_of_full_circle = (2 * math.pi) / 8

    def __init__(
        self, snake_head: List[int], snake_body: List[List[int]], food_pos: List[int], qdirection: int, action: int
    ):
        self.snake_head = snake_head.copy()
        self.snake_body = snake_body.copy()
        self.food_pos = food_pos.copy()
        self.qdirection = qdirection
        self.action = action

    def __str__(self):
        return str(self.snake_head, tuple(self.snake_body), self.food_pos, self.qdirection, self.action)

    def __hash__(self):
        # Total 15bit = 2^15 states

        # claculate free space around head 3x3 (without head) = 8 bit
        # Alternative would be to claculate free space around head 5x5 (without head and diagonals) = 16 bit
        view_repr = ''
        for x in range(-1, 2):
            for y in range(-1, 2):
                # skip head and all diagonals
                if x == 0 and y == 0:
                    continue
                x_cord = self.snake_head[0] + x * 10
                y_cord = self.snake_head[1] + y * 10
                if (
                    [x_cord, y_cord] in self.snake_body
                    or x_cord < 0
                    or x_cord > window_width_scaled - 10
                    or y_cord < 0
                    or y_cord > window_height_scaled - 10
                ):
                    view_repr += '1'
                else:
                    view_repr += '0'

        angle_to_food = math.atan2(
            self.food_pos[1] - self.snake_head[1], self.food_pos[0] - self.snake_head[0])
        food_dir_repr = int((angle_to_food + math.pi) /
                            self.one_eighth_of_full_circle)
        return int(f'{view_repr}{food_dir_repr:03b}{self.qdirection:02b}{self.action:02b}', 2)


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
fpscount = 0
fps_count = 0

# Setze Snake-Startposition und -Geschwindigkeit
snake_head = [400, 300]
snake_body = [[400, 300], [390, 300], [380, 300], [370, 300], [360, 300]]
snake_speed = pygame.math.Vector2(1, 0)
body_count = 0
body_dist = 0


def count_body(snake_body):
    """Zählt die Anzahl der Segmente im Körper der Schlange."""
    return len(snake_body)


# Setze Richtungsvariablen
direction = 'RIGHT'
distance = 0.0
distance2 = 0.0
qdirection = 3
change_to = direction
action = 1

# Setze Punkte
score = 0
reward = 0

# Setze variablen auf False
game_is_over = 0
food_eaten = 0

# Setze Schriftart und -farbe für Punktzahl
font = pygame.font.Font('freesansbold.ttf', 18)
score_font = pygame.font.Font('freesansbold.ttf', 28)
score_color = pygame.Color('white')

# Setze Game Over-Text
game_over_font = pygame.font.Font('freesansbold.ttf', 48)
game_over_color = pygame.Color('white')


def spawn_food():
    while True:
        food_pos = [random.randrange(
            1, (window_width_scaled // 20)) * 20, random.randrange(1, (window_height_scaled // 20)) * 20]
        if food_pos not in snake_body:
            return food_pos


# Setze Futter-Startposition
food_pos = spawn_food()
food_spawn = True

"""try:
    with open('scores.txt', 'r') as f:
        scores = []
        for line in f:
            s, _ = line.split('\t')
            scores.append(int(s))
except FileNotFoundError:
        with open('scores.txt', 'w') as f:
            scores = [0] """

with open('scores.txt', 'r') as f:
        scores = []
        for line in f:
            s, _, _ = line.split('\t')
            scores.append(int(s))

def restart_game():
    global snake_head, snake_body, snake_speed, direction, change_to, score, food_pos, food_spawn, game_is_over
    snake_head = [400, 300]
    snake_body = [[400, 300], [390, 300], [380, 300], [370, 300], [360, 300]]
    snake_speed = pygame.math.Vector2(1, 0)
    food_pos = spawn_food()
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0
    game_is_over = 0


def game_over():
    global game_is_over
    global reward

    reward = -30# - (body_count - 4) * 0.01
    update_q_table(q_table, state, action, reward,
                   next_state, learning_rate, discount_factor)
    # save_state_to_file(state)
    # save_state2_to_file(next_state)
    #write_state_to_file2(snake_head, snake_body, body_count, food_pos, qdirection, action, game_is_over, distance2, reward, body_dist)
    # time.sleep(2)

    

     

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
    screen.blit(highscore_text, (window_width_scaled / 3, window_height_scaled / 3))
    screen.blit(score_text, (window_width_scaled / 3, window_height_scaled / 3 + 50))
    pygame.display.update()
    time.sleep(0.025)
    # Rufe die Funktion auf, wenn das Spiel beendet wird
    save_score(score, counter)
    restart_game()
    game_is_over = 0


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
      
      now = datetime.datetime.now()
      dates.append(now.strftime('%Y-%m-%d %H:%M:%S'))
      counters.append(counter)
      # Schreibe alle Scores und Datumsangaben in die Textdatei
      for s, d, c in zip(scores, dates, counters):
        f.write(f"{s}\t{d}\t{c}\n")


def test_direction():
    global direction, food_pos, snake_head, change_to, action

    x_distance = food_pos[0] - snake_head[0]
    y_distance = food_pos[1] - snake_head[1]

    # Überprüfe, ob sich Snake horizontal oder vertikal bewegt
    if x_distance == 0:
        if y_distance > 0:
            if direction != 'UP':
                # Wenn das Futter unterhalb von Snake ist
                # change_to = 'DOWN'
                action = 2
            else:
                # change_to = 'LEFT'
                action = 3
        else:
            if direction != 'DOWN':
                # Wenn das Futter oberhalb von Snake ist
                # change_to = 'UP'
                action = 0
            else:
                # change_to = 'LEFT'
                action = 3
    elif y_distance == 0:
        if x_distance > 0:
            if direction != 'LEFT':
                # Wenn das Futter rechts von Snake ist
                # change_to = 'RIGHT'
                action = 1
            else:
                # change_to = 'UP'
                action = 0
        else:
            if direction != 'RIGHT':
                # Wenn das Futter links von Snake ist
                # change_to = 'LEFT'
                action = 3
            else:
                # change_to = 'UP'
                action = 0
    else:
        # Wenn sich das Futter diagonal zu Snake befindet
        if direction in ('UP', 'DOWN'):
            if x_distance > 0:
                # Wenn das Futter rechts von Snake ist
                # change_to = 'RIGHT'
                action = 1
            else:
                # Wenn das Futter links von Snake ist
                # change_to = 'LEFT'
                action = 3
        elif direction in ('LEFT', 'RIGHT'):
            if y_distance > 0:
                # Wenn das Futter unterhalb von Snake ist
                # change_to = 'DOWN'
                action = 2
            else:
                # Wenn das Futter oberhalb von Snake ist
                # change_to = 'UP'
                action = 0


def set_body_dist(snake_head, snake_body, direction):
    # Set the default value of body_dist to 0
    body_dist = 0

    # Check the position of each body segment relative to the snake head
    for segment in snake_body:
        # Check if the segment is in the same row or column as the snake head
        if direction == 'UP' or direction == 'DOWN':
            if segment[0] == snake_head[0]:
                dist = snake_head[1] - segment[1]
                if direction == 'UP' and dist > 0 and dist <= window_width_scaled:
                    body_dist = max(body_dist, 1 - dist/window_width_scaled)
                elif direction == 'DOWN' and dist < 0 and dist >= -window_width_scaled:
                    body_dist = max(body_dist, 1 + dist/window_width_scaled)
        elif direction == 'LEFT' or direction == 'RIGHT':
            if segment[1] == snake_head[1]:
                dist = snake_head[0] - segment[0]
                if direction == 'LEFT' and dist > 0 and dist <= window_width_scaled:
                    body_dist = max(body_dist, 1 - dist/window_width_scaled)
                elif direction == 'RIGHT' and dist < 0 and dist >= -window_width_scaled:
                    body_dist = max(body_dist, 1 + dist/window_width_scaled)

    # Return the calculated value of body_dist
    return body_dist


def get_qdirection(direction):
    global qdirection

    if direction == 'DOWN':
        qdirection = 0
    if direction == 'LEFT':
        qdirection = 1
    if direction == 'UP':
        qdirection = 2
    if direction == 'RIGHT':
        qdirection = 3


def get_distance():
    global distance
    distance = round(math.sqrt(
        (snake_head[0] - food_pos[0]) ** 2 + (snake_head[1] - food_pos[1]) ** 2))


def get_distance2():
    global distance2
    distance2 = round(math.sqrt(
        (snake_head[0] - food_pos[0]) ** 2 + (snake_head[1] - food_pos[1]) ** 2))


def get_reward(distance, distance2, body_count, body_dist):
    global reward
    reward = 0

    dist1 = distance
    dist2 = distance2

    # Wenn die Distanz zum Futter im aktuellen Schritt kürzer ist als im vorherigen Schritt, belohne die Ki
    #if dist2 < dist1:
    #    reward = 0.1 + (body_count - 4) * 0.01

    # if dist1 < dist2:
    #    reward = -1 - distance2 * 0.001 - (body_count -4) * 0.01

    if snake_head[0] == food_pos[0] and snake_head[1] == food_pos[1]:
        reward += 5# + (body_count - 4) * 0.1

    reward -= body_dist

    #if body_dist == 0:
    #    reward += (body_count - 4) * 0.01

    return reward


def create_q_table(num_states, num_actions):
    q_table = np.zeros((num_states, num_actions))
    return q_table


def load_q_table():
    try:
        with open('q_table.json', 'r') as f:
            q_table = np.array(json.load(f))
    except FileNotFoundError:
        q_table = create_q_table(num_states, num_actions)
    return q_table


# Definiere die Parameter für die Funktion


num_states = 2**15
num_actions = 4
discount_factor = 0.9
learning_rate = 0.1
epsilon = 0.0
q_table = load_q_table()


def read_ki_info():

    try:
        with open('ki_info.txt', 'r') as f:
            lines = f.readlines()
            last_line = lines[-1].strip()
            counter = int(last_line.split()[0])

    except FileNotFoundError:
        counter = 0

    return counter


counter = read_ki_info()
randact = 0


def update_q_table(q_table, state: State, action, reward, next_state: State, learning_rate, discount_factor):
    # Extrahieren des aktuellen Zustands und der nächsten Zustände
    state_idx = hash(state) % num_states
    next_state_idx = hash(next_state) % num_states

    # Aktualisierung des Q-Werts für den ausgewählten Zustand und die ausgewählte Aktion
    old_q_value = q_table[state_idx][action]
    next_max_q_value = np.max(q_table[next_state_idx])
    temporal_difference = reward + discount_factor * next_max_q_value - old_q_value
    new_q_value = old_q_value + learning_rate * temporal_difference
    q_table[state_idx][action] = new_q_value

    return q_table


def select_action(q_table, state: State, epsilon):
    global action
    global randact
    state_idx = hash(state) % num_states

    # Wähle zufällig eine Aktion mit einer Wahrscheinlichkeit von epsilon
    if np.random.uniform(0, 1) < epsilon:
        action = np.random.randint(0, 4)
        randact = 1
    # Wähle die Aktion mit dem höchsten Q-Wert
    else:
        action = np.argmax(q_table[state_idx])
        randact = 0

    return action


def safe_ki_info(counter):

    with open('ki_info.txt', 'w') as f:
        f.write(f"{counter}\n")


def save_state_to_file(state: State):
    with open('qstate.txt', 'a') as file:
        file.write(str(state))


def save_state2_to_file(next_state: State):
    with open('qstate2.txt', 'a') as file:
        file.write(str(next_state))


def write_state_to_file(snake_head, snake_body, food_pos, qdirection, action, game_is_over, distance):
    with open('ki_state.txt', 'a') as f:
        f.write('State:\n')
        f.write(f'snake_head: {snake_head}\n')
        f.write(f'snake_body: {snake_body}\n')
        f.write(f'food_pos: {food_pos}\n')
        f.write(f'direction: {qdirection}\n')
        f.write(f'action: {action}\n')
        f.write(f'game_is_over: {game_is_over}\n')
        f.write(f'distance: {distance}\n')
        f.write('\n')





def write_state_to_file2(
    snake_head,
    snake_body,
    body_count,
    food_pos,
    qdirection,
    action,
    game_is_over,
    distance2,
    reward,
    body_dist,
):
    with open('ki_state.txt', 'a') as f:
        f.write('State2:\n')
        f.write(f'snake_head: {snake_head}\n')
        f.write(f'snake_body: {snake_body}\n')
        f.write(f'snake_body: {body_count}\n')
        f.write(f'food_pos: {food_pos}\n')
        f.write(f'direction: {qdirection}\n')
        f.write(f'action: {action}\n')
        f.write(f'game_is_over: {game_is_over}\n')
        f.write(f'distance: {distance2}\n')
        f.write(f'reward: {reward}\n')
        f.write(f'body_dist: {body_dist}\n')

        f.write('\n')

running = True

# Setze Hauptschleife
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                with open('q_table.json', 'w') as f:
                    json.dump(q_table.tolist(), f)
                safe_ki_info(counter)
                runing = False
                exec(open('menu.py').read())
                #pygame.quit()
                #sys.exit(subprocess.call(["python", "run.py"]))

    counter += 1
    epsilon = math.exp(-counter * 0.00002)
    if epsilon <= 0.0001:
        epsilon = 0
    #if counter >= 2500000:
    #    epsilon = 0
    get_qdirection(direction)
    state = State(snake_head, snake_body, food_pos, qdirection, action)
    get_distance()
    #write_state_to_file(snake_head, snake_body, food_pos, qdirection, action, game_is_over, distance)
    # save_state_to_file(state)
    # test_direction()
    select_action(q_table, state, epsilon)

    if action == 0:
        change_to = 'UP'
    if action == 1:
        change_to = 'RIGHT'
    if action == 2:
        change_to = 'DOWN'
    if action == 3:
        change_to = 'LEFT'

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

    get_distance2()
    get_qdirection(direction)
    body_count = count_body(snake_body)
    body_dist = set_body_dist(snake_head, snake_body, direction)
    get_reward(distance, distance2, body_count, body_dist)

    next_state = State(snake_head, snake_body, food_pos, qdirection, action)
    #write_state_to_file2(snake_head, snake_body, body_count, food_pos, qdirection, action, game_is_over, distance2, reward, body_dist)
    if counter <= 5000000:
        update_q_table(q_table, state, action, reward,
                       next_state, learning_rate, discount_factor)
    #safe_ki_info(counter, reward, randact, epsilon)

    # Füge neues Snake-Segment hinzu, falls Snake Futter gefressen hat
    snake_body.insert(0, list(snake_head))
    if snake_head[0] == food_pos[0] and snake_head[1] == food_pos[1]:
        score += 1

        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = spawn_food()
    food_spawn = True

    screen.fill(bg_color)
    # Zeichne den Bildschirmrand
    pygame.draw.rect(screen, pygame.Color('purple'), pygame.Rect(0, 0, screen_width, 1))  # Obere Kante
    pygame.draw.rect(screen, pygame.Color('purple'), pygame.Rect(0, 0, 1, screen_height))  # Linke Kante
    pygame.draw.rect(screen, pygame.Color('purple'), pygame.Rect(screen_width-1, 0, 1, screen_height))  # Rechte Kante
    pygame.draw.rect(screen, pygame.Color('purple'), pygame.Rect(0, screen_height-1, screen_width, 1))  # Untere Kante
    # Zeichne Snake
    for i, pos in enumerate(snake_body):
        if i == 0:  # Wenn es sich um den Kopf handelt
            pygame.draw.rect(screen, pygame.Color('red'),
                             pygame.Rect(pos[0], pos[1], 10, 10))
        else:  # Wenn es sich um den Körper handelt
            pygame.draw.rect(screen, pygame.Color('brown'),
                             pygame.Rect(pos[0], pos[1], 10, 10))

    # Zeichne Futter
    pygame.draw.rect(screen, pygame.Color('green'),
                     pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Zeichne Punktzahl
    score_font = font.render('Score: ' + str(score), True, score_color)
    screen.blit(score_font, [0, 0])

    # Zeichne reward
    score_font = font.render('rew: {:.3f}'.format(reward), True, score_color)
    screen.blit(score_font, [400, 0])

    # Zeichne random
    score_font = font.render('cnt: ' + str(counter), True, score_color)
    screen.blit(score_font, [200, 0])

    # Zeichne epsilon
    score_font = font.render('eps: {:.4f}'.format(epsilon), True, score_color)
    screen.blit(score_font, [600, 0])

    # Überprüfe, ob Snake sich selbst gebissen hat
    if snake_head[0] < 0 or snake_head[0] > window_width_scaled - 10:
        game_over()
    if snake_head[1] < 0 or snake_head[1] > window_height_scaled - 10:
        game_over()

    for block in snake_body[1:]:
        if snake_head[0] == block[0] and snake_head[1] == block[1]:
            game_over()

    pygame.display.update()

    if fps_count >= 300:
        fpscount = 0
        fps_count = 0
    if counter <= 5000000:

        if counter % 100000 == 0:
            fps.tick(20)
            fpscount = 1

        else:
            fps.tick(600)

    else:
        fps.tick(20)

    if fpscount == 1:
        fps.tick(20)
        fps_count += 1
