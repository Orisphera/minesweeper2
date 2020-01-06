import os
import pygame
import random
import sqlite3
import sys
import time


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


# Based on MineSweeper by Uee
class MineSweeper:
    # CONSTRUCTOR
    def __init__(self, cols=9, rows=9, mines=10):
        self.cols = cols
        self.rows = rows
        self.mines = mines
        self.grid = None
        self.open = [[False] * self.cols for _ in range(self.rows)]
        self.closed_count = rows * cols
        self.game_over = False
        self.player_won = None
        self.flagged = [[False] * self.cols for _ in range(self.rows)]
        self.flag_count = 0
        self.start_time = None
        self.time = None

    # MINE SWEEPER FUNCTIONS
    # 'B' -> Bomb
    def place_mines(self):
        i = 0
        while i != self.mines:
            x = random.randint(0, self.cols - 1)
            y = random.randint(0, self.rows - 1)

            if self.grid[y][x] == 'B':
                continue
            else:
                self.grid[y][x] = 'B'
                i += 1

    # Checks The 8 Surrounding Blocks Around The Middle Tile - MSGrid[y][x],
    # And Count The Number Of Mines Found Around It. The Number Found Will Replace The Middle Tile -
    # MSGrid[y][x] Original Value.
    def place_numbers(self):
        for r in range(0, self.rows):
            for c in range(0, self.cols):
                if self.grid[r][c] == '#':
                    self.grid[r][c] = self.number_to_char(self.sur_mines(r, c))

    def move(self, r, c):
        if self.game_over:
            return
        if self.flagged[r][c]:
            return
        if self.grid is None:
            self.set_grid()
            for r1, c1 in self.sur_cells(r, c):
                self.grid[r1][c1] = 'B'
            self.place_mines()
            for r1, c1 in self.sur_cells(r, c):
                self.grid[r1][c1] = '#'
            self.place_numbers()
            self.start_time = time.time()
        if self.open[r][c]:
            return
        self.open[r][c] = True
        self.closed_count -= 1
        if self.grid[r][c] == ' ':
            for r1, c1 in self.sur_cells(r, c):
                if self.flagged[r1][c1]:
                    self.flagged[r1][c1] = False
                    self.flag_count -= 1
                self.move(r1, c1)
        elif self.grid[r][c] == 'B':
            self.player_won = False
            self.game_over = True

    def flag(self, r, c):
        if self.open[r][c]:
            return
        if self.flagged[r][c]:
            self.flagged[r][c] = False
            self.flag_count -= 1
        else:
            self.flagged[r][c] = True
            self.flag_count += 1

    def move_nearby(self, r, c):
        if not self.open[r][c]:
            return
        if self.grid[r][c] == ' ':
            return
        remaining_mines = int(self.grid[r][c])
        for r1, c1 in self.sur_cells(r, c):
            if self.flagged[r1][c1]:
                remaining_mines -= 1
        if not remaining_mines:
            for r1, c1 in self.sur_cells(r, c):
                if not self.flagged[r1][c1]:
                    self.move(r1, c1)

    def check_win(self):
        if self.closed_count == self.mines:
            self.time = self.get_time()
            self.player_won = True
            self.game_over = True

    # HELPER FUNCTIONS
    # Determine The Number Of Surrounding Mines/Bombs Around The Given Point X, Y

    def sur_cells(self, r, c):
        for r1 in range(max(r - 1, 0), min(r + 2, self.rows)):
            for c1 in range(max(c - 1, 0), min(c + 2, self.cols)):
                yield r1, c1

    def sur_mines(self, r, c):
        ans = 0
        for r1, c1 in self.sur_cells(r, c):
            if self.grid[r1][c1] == 'B':
                ans += 1
        return ans

    @staticmethod
    def number_to_char(num):
        return str(num) if num else ' '

    def get_time(self):
        return 0 if self.start_time is None else time.time() - self.start_time

    def set_grid(self):
        self.grid = [['#' for _ in range(self.cols)] for _ in range(self.rows)]


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    screen.fill((0, 0, 0))
    with open('intro.txt') as f:
        intro_text = f.read().rstrip('\n').split('\n')
    text_coord = 50
    text_rects = []
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        text_rects.append(intro_rect)
    pygame.display.flip()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for rect, ans in zip(text_rects[-3:], (('easy', 10, 8, 10),
                                                   ('medium', 18, 14, 40),
                                                   ('hard', 24, 20, 99))):
                if rect.top <= y <= rect.top + rect.height and \
                        rect.x <= x <= rect.x + rect.width:
                    return ans


def play(diff_id, cols, rows, mines):

    def display():
        screen.fill((0, 0, 0))
        for r in range(rows):
            for c in range(cols):
                text = ' '
                text_color = 0, 0, 0
                if ms.open[r][c]:
                    ch = ms.grid[r][c]
                    if ch == 'B':
                        bg_color = 255, 0, 0
                        im_name = 'bomb.png'
                    else:
                        bg_color = (215, 184, 153) if (r + c) % 2 else (229, 194, 159)
                        if ch == ' ':
                            im_name = None
                        else:
                            im_name = None
                            text = ch
                            text_color = ((0, 0, 0),
                                          (0, 0, 255),
                                          (0, 255, 0),
                                          (255, 0, 0),
                                          (64, 0, 128),
                                          (128, 255, 0),
                                          (255, 255, 0),
                                          (255, 128, 0),
                                          (255, 0, 0))[int(ch)]
                else:
                    bg_color = (162, 209, 73) if (r + c) % 2 else (170, 215, 81)
                    if ms.flagged[r][c]:
                        if ms.game_over and ms.grid[r][c] != 'B':
                            im_name = 'cross.png'
                        else:
                            im_name = 'flag.png'
                    elif ms.game_over and ms.grid[r][c] == 'B':
                        im_name = 'bomb.png'
                    else:
                        im_name = None
                pygame.draw.rect(screen, bg_color, (left + cell * c, upper + cell * r, cell, cell))
                if im_name is not None:
                    image = pygame.transform.scale(load_image(im_name, -1), (cell, cell))
                    im_rect = image.get_rect()
                    im_rect.top = upper + cell * r
                    im_rect.x = left + cell * c
                    screen.blit(image, im_rect)
                text_rendered = font.render(text, 1, text_color)
                text_rect = text_rendered.get_rect()
                text_rect.top = upper + cell * r + (cell - text_rect.height) // 2
                text_rect.x = left + cell * c + (cell - text_rect.width) // 2
                screen.blit(text_rendered, text_rect)
        if not ms.game_over:
            text = (f'Мин: {mines}',
                    f'Помеченых клеток: {ms.flag_count}',
                    f'Время: {int(ms.get_time())} с')
        elif ms.player_won:
            text = (f"Вы выиграли! Время: {ms.time} с",
                    'Нажмите для продолжения')
        else:
            text = ("Вы проиграли!",
                    'Нажмите, чтобы играть снова')
        text_coord = 10
        for string in text:
            string_rendered = font.render(string, 1, pygame.Color('white'))
            string_rect = string_rendered.get_rect()
            string_rect.top = text_coord
            string_rect.x = 10
            screen.blit(string_rendered, string_rect)
            text_coord += 20
        pygame.display.flip()

    def on_mouse_button_down():
        x, y = event.pos
        r, c = (y - upper) // cell, (x - left) // cell
        if 0 <= r < rows and 0 <= c < cols:
            if event.button == 3:
                ms.flag(r, c)
            else:
                ms.move_nearby(r, c)
                ms.move(r, c)
                ms.check_win()

    ms = MineSweeper(cols, rows, mines)
    upper = 100
    left = 10
    cell = 20
    display()
    while not ms.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                on_mouse_button_down()
        display()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            break
    if ms.player_won:
        record(diff_id, ms.time)


def record(diff_id, new_time):
    con = sqlite3.connect('records.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS records ('
                ' difficulty TEXT,'
                ' name TEXT,'
                ' time REAL)')
    if cur.execute(f'SELECT time FROM records'
                   f' WHERE difficulty = "{diff_id}"'
                   f' AND time >= {new_time}').fetchall():
        return
    name = ''
    while True:
        screen.fill((0, 0, 0))
        text = f'Введите имя для таблицы рекордов: {name}'
        text_rendered = font.render(text, 1, (255, 255, 255))
        text_rect = text_rendered.get_rect()
        text_rect.top = 100
        text_rect.x = 10
        screen.blit(text_rendered, text_rect)
        pygame.display.flip()
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_BACKSPACE:
                name = name[:-1]
            elif key == pygame.K_RETURN:
                break
            else:
                key_name = pygame.key.name(key)
                name += key_name
    cur.execute(f'INSERT INTO records(diff_id, name, time)'
                f' VALUES({diff_id}, {name}, {new_time})')


pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
font = pygame.font.Font(None, 30)
while True:
    play(*start_screen())
