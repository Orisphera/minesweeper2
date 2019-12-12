import pygame
import random
import sys


# By Uee
class MineSweeper(object):
    # Columns And Rows Variables
    Columns, Rows = 0, 0
    # Number of Mines Variable
    NoOfMines = 0
    # Mine Sweeper Grid Variable
    MSGrid = None
    # Random Integer Variable
    RandInt = random.randint

    # CONSTRUCTOR
    def __init__(self, Columns=9, Rows=9, NoOfMines=10):
        self.Columns = Columns
        self.Rows = Rows
        self.NoOfMines = NoOfMines

    # MINE SWEEPER FUNCTIONS
    # 'B' -> Bomb
    def PlaceMines(self, Char='B'):
        i = 0
        while i != self.NoOfMines:
            x = self.RandInt(0,
                             self.Columns - 1)
            y = self.RandInt(0, self.Rows -
                             1)

            if (self.MSGrid[y][x] == Char):
                continue
            else:
                self.MSGrid[y][x] = Char
                i += 1

    # Checks The 8 Surrounding Blocks Around The Middle Tile - MSGrid[y][x],
    # And Count The Number Of Mines Found Around It. The Number Found Will Replace The Middle Tile -
    # MSGrid[y][x] Original Value.
    def PlaceNumbers(self):
        for r in range(0, self.Rows):
            for c in range(0,
                           self.Columns):
                if (self.MSGrid[r][c] ==
                        'B' or
                        str.isdigit(self.MSGrid[r]
                                    [c])):
                    continue
                else:
                    self.MSGrid[r][c] = \
                        self.NoOfSurMines(r, c)

    # HELPER FUNCTIONS
    # Determine The Number Of Surrounding Mines/Bombs Around The Given Point X, Y
    def NoOfSurMines(self, y=0, x=0):
        return self.Left(x - 1, y) + \
               self.Right(x + 1, y) + self.Up(x, y
                                              + 1) + self.Down(x, y - 1) + \
               self.TopRight(x + 1, y + 1) + \
               self.BottomRight(x + 1, y - 1) + \
               self.TopLeft(x - 1, y + 1) + \
               self.BottomLeft(x - 1, y - 1)

    # Check The Block Left Of The Middle Tile
    def Left(self, x=0, y=0):
        return 0 if (x < 0 or self.MSGrid[y][x] != 'B') else 1

    # Check The Block Right Of The Middle Tile
    def Right(self, x=0, y=0):
        return 0 if (x >= self.Columns or self.MSGrid[y][x] != 'B') else 1

    # Check The Block Above The Middle Tile
    def Up(self, x=0, y=0):
        return 0 if (y >= self.Rows or self.MSGrid[y][x] != 'B') else 1

    # Check The Block Below The Middle Tile
    def Down(self, x=0, y=0):
        return 0 if (y < 0 or self.MSGrid[y][x] != 'B') else 1

    # Check The Top Right Block From The Middle Tile
    def TopRight(self, x=0, y=0):
        return 0 if (x >= self.Columns or y >= self.Rows or self.MSGrid[y][x] != 'B') else 1

    # Check The Bottom Right Block From The Middle Tile
    def BottomRight(self, x=0, y=0):
        return 0 if (x >= self.Columns or y < 0 or self.MSGrid[y][x] != 'B') else 1

    # Check The Top Left Block From The Middle Tile
    def TopLeft(self, x=0, y=0):
        return 0 if (x < 0 or y >= self.Rows or self.MSGrid[y][x] != 'B') else 1

    # Check The Bottom Left Block From The Middle Block
    def BottomLeft(self, x=0, y=0):
        return 0 if (x < 0 or y < 0 or
                     self.MSGrid[y][x] != 'B') else 1

    # Display The Mine Sweeper Grid
    def DisplayGrid(self):
        line = ""
        for r in range(0, self.Rows):
            for c in range(0, self.Columns):
                line += str(self.MSGrid[r][c]) + " "
            print(line)
            line = ""

    # GETTER'S AND SETTER'S
    def SetMSGrid(self, Char='#'):
        self.MSGrid = [[Char for i in range(self.Columns)] for i in range(self.Rows)]


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
    def display():
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 30)
        for r in range(rows):
            for c in range(cols):
                if state[r][c] == 'open':
                    ch = str(MS.MSGrid[r][c])
                elif state[r][c] == 'flag':
                    if player_lost and MS.MSGrid[r][c] != 'B':
                        ch = 'X'
                    else:
                        ch = 'F'
                elif player_lost and MS.MSGrid[r][c] == 'B':
                    ch = 'O'
                else:
                    ch = '#'
                string_rendered = font.render(ch, 1, pygame.Color('white'))
                text_rect = string_rendered.get_rect()
                text_rect.top = upper + cell * r
                text_rect.x = left + cell * c
                screen.blit(string_rendered, text_rect)
        pygame.display.flip()

    def open_cell(r, c):
        nonlocal player_lost, playing
        if state[r][c] == 'none':
            state[r][c] = 'open'
            if MS.MSGrid[r][c] == 'B':
                player_lost = True
                playing = False
            elif MS.MSGrid[r][c] == ' ':
                for r1 in range(max(r - 1, 0), min(r + 2, rows)):
                    for c1 in range(max(c - 1, 0), min(c + 2, cols)):
                        open_cell(r1, c1)

    rows, cols, mines = 14, 18, 40
    closed_cells = rows * cols
    MS = MineSweeper(cols, rows, mines)
    MS.SetMSGrid()
    MS.PlaceMines()
    MS.PlaceNumbers()
    state = [['none'] * cols for _ in range(rows)]
    upper = 100
    left = 10
    cell = 20
    player_lost = False
    playing = True
    display()
    while playing:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            r, c = (y - upper) // cell, (x - left) // cell
            if 0 <= r < rows and 0 <= c < cols:
                if event.button == 3:
                    if state[r][c] == 'none':
                        state[r][c] = 'flag'
                    elif state[r][c] == 'flag':
                        state[r][c] = 'none'
                else:
                    if closed_cells == rows * cols:
                        while MS.MSGrid[r][c] != ' ':
                            MS.SetMSGrid()
                            MS.PlaceMines()
                            MS.PlaceNumbers()
                    open_cell(r, c)
                    if closed_cells == mines:
                        playing = False
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
