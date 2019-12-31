import pygame
import random
import sys


# Based on MineSweeper by Uee
class MineSweeper():
    # Mine Sweeper Grid Variable
    MSGrid = None

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
        if self.grid is None:
            self.setgrid()
            for r1, c1 in self.sur_cells(r, c):
                self.grid[r1][c1] = 'B'
            self.place_mines()
            for r1, c1 in self.sur_cells(r, c):
                self.grid[r1][c1] = '#'
            self.place_numbers()
        if self.open[r][c]:
            return
        self.open[r][c] = True
        self.closed_count -= 1
        if self.grid[r][c] == ' ':
            for r1, c1 in self.sur_cells(r, c):
                self.move(r1, c1)
        elif self.grid[r][c] == 'B':
            self.player_won = False
            self.game_over = True

    def check_win(self):
        if self.closed_count == self.mines:
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

    def number_to_char(self, num):
        return str(num) if num else ' '

    # GETTER'S AND SETTER'S
    def setgrid(self):
        self.grid = [['#' for i in range(self.cols)] for i in range(self.rows)]


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    with open('intro.txt') as f:
        intro_text = f.read().split('\n')
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.display.flip()


def play():
    font = pygame.font.Font(None, 30)

    def display():
        screen.fill((0, 0, 0))
        for r in range(rows):
            for c in range(cols):
                if ms.open[r][c]:
                    ch = ms.grid[r][c]
                    if ch == 'B':
                        color = 255, 0, 0
                    elif ch == ' ':
                        color = 255, 255, 0
                    else:
                        color = 255, 256 - int(ch) * 32, 0
                elif state[r][c] == 'flag':
                    if ms.game_over and ms.grid[r][c] != 'B':
                        ch = 'X'
                    else:
                        ch = 'F'
                    color = 255, 0, 0
                elif ms.game_over and ms.grid[r][c] == 'B':
                    ch = 'O'
                    color = 255, 0, 0
                else:
                    ch = '#'
                    color = 0, 255, 0
                string_rendered = font.render(ch, 1, color)
                text_rect = string_rendered.get_rect()
                text_rect.top = upper + cell * r
                text_rect.x = left + cell * c
                screen.blit(string_rendered, text_rect)
        if ms.game_over:
            string1 = f"Вы {'вы' if ms.player_won else 'про'}играли!"
            string2 = 'Нажмите, чтобы играть снова'
        else:
            string1 = f'Мин: {mines}'
            string2 = f'Помеченых клеток: {marked_cells}'
        string1_rendered = font.render(string1, 1, pygame.Color('white'))
        text1_rect = string1_rendered.get_rect()
        text1_rect.top = 10
        text1_rect.x = 10
        screen.blit(string1_rendered, text1_rect)
        string2_rendered = font.render(string2, 1, pygame.Color('white'))
        text2_rect = string2_rendered.get_rect()
        text2_rect.top = 30
        text2_rect.x = 10
        screen.blit(string2_rendered, text2_rect)
        pygame.display.flip()

    rows, cols, mines = 14, 18, 40
    closed_cells = rows * cols
    marked_cells = 0
    ms = MineSweeper(cols, rows, mines)
    state = [['none'] * cols for _ in range(rows)]
    upper = 100
    left = 10
    cell = 20
    display()
    while not ms.game_over:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            r, c = (y - upper) // cell, (x - left) // cell
            if 0 <= r < rows and 0 <= c < cols:
                if event.button == 3:
                    if not ms.open[r][c]:
                        if state[r][c] == 'none':
                            state[r][c] = 'flag'
                            marked_cells += 1
                        elif state[r][c] == 'flag':
                            state[r][c] = 'none'
                            marked_cells -= 1
                else:
                    if state[r][c] == 'none':
                        if ms.open[r][c] and ms.grid[r][c].isdigit():
                            remaining_mines = int(ms.grid[r][c])
                            for r1, c1 in ms.sur_cells(r, c):
                                if state[r1][c1] == 'flag':
                                    remaining_mines -= 1
                            if not remaining_mines:
                                for r1, c1 in ms.sur_cells(r, c):
                                    if state[r1][c1] != 'flag':
                                        ms.move(r1, c1)
                                        state[r1][c1] = 'none'
                        ms.move(r, c)
            display()


pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
start_screen()
while True:
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            break
    play()
