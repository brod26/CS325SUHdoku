import pygame
from sudoku_methods import solve_sudoku_board, legal_move_check, verify_solution
import time
from random import sample
pygame.font.init()

# Author: Bryan Rodriguez-Andrade
# Date: 12/7/2020
# Description: CS 325, Portfolio Project


# reference code for solutions below taken from
# stack overflow: https://stackoverflow.com/questions/17605898/sudoku-checker-in-python
# geeks for geeks: https://www.geeksforgeeks.org/sudoku-backtracking-7/
# techwithtim: https://www.techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/
# medium.com: https://medium.com/swlh/this-is-how-to-create-a-simple-minesweeper-game-in-python-af02077a8de


class Grid:

    sudoku_board = [[0 for i in range(9)] for k in range(9)]

    def __init__(self, rows, columns, width, height):
        self.rows = rows
        self.columns = columns
        self.width = 540
        self.height = 540
        self.model = None
        self.selected = None
        self.base = 3
        self.side = self.base*self.base
        self.create_board()
        self.boxes = [[Box(self.sudoku_board[i][j], i, j, 540, 540)
                    for j in range(columns)] for i in range(rows)]

    def pattern(self, r, c):
        return (self.base*(r % self.base)+r//self.base+c) % self.side

    def shuffle(self, s):
        return sample(s, len(s))

    def create_board(self):
        rBase = range(self.base)
        rows = [g*self.base +
                r for g in self.shuffle(rBase) for r in self.shuffle(rBase)]
        cols = [g*self.base +
                c for g in self.shuffle(rBase) for c in self.shuffle(rBase)]
        nums = self.shuffle(range(1, self.base*self.base+1))

        # produce board using randomized baseline pattern
        sudoku_board = [[nums[self.pattern(r, c)] for c in cols] for r in rows]

        squares = self.side*self.side
        empties = squares * 3//4
        for p in sample(range(squares), empties):
            sudoku_board[p//self.side][p % self.side] = 0

        self.sudoku_board = sudoku_board

    def solve_board(self):
        self.sudoku_board = solve_sudoku_board(self.sudoku_board)

    def set_model(self):
        self.model = [[self.boxes[i][j].value for j in range(
            self.columns)] for i in range(self.rows)]

    def make_move(self, val):
        row, column = self.selected
        if self.boxes[row][column].value == 0:
            self.boxes[row][column].set(val)
            self.set_model()

            if legal_move_check(self.model, val, (row, column)) and solve_sudoku_board(self.model):
                return True
            else:
                self.boxes[row][column].set(0)
                self.boxes[row][column].set_temp(0)
                self.set_model()
                return False

    def temp_draw(self, val):
        row, column = self.selected
        self.boxes[row][column].set_temp(val)

    def draw(self, win):
        spacing = self.width/9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                padding = 4
            else:
                padding = 1
            pygame.draw.line(win, (0, 0, 0), (0, i*spacing),
                            (self.width, i*spacing), padding)
            pygame.draw.line(win, (0, 0, 0), (i * spacing, 0),
                             (i * spacing, self.height), padding)

        for i in range(self.rows):
            for j in range(self.columns):
                self.boxes[i][j].draw(win)

    def draw_solved_board(self, win):
        self.boxes = [[Box(self.sudoku_board[i][j], i, j, 540, 540)
                    for j in range(self.columns)] for i in range(self.rows)]
        spacing = self.width/9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                padding = 4
            else:
                padding = 1
            pygame.draw.line(win, (0, 0, 0), (0, i*spacing),
                            (self.width, i*spacing), padding)
            pygame.draw.line(win, (0, 0, 0), (i * spacing, 0),
                             (i * spacing, self.height), padding)

        for i in range(self.rows):
            for j in range(self.columns):
                self.boxes[i][j].draw(win)

    def make_selection(self, row, column):
        for i in range(self.rows):
            for j in range(self.columns):
                self.boxes[i][j].selected = False
        self.boxes[row][column].selected = True
        self.selected = (row, column)

    def clear_box(self):
        row, column = self.selected
        if self.boxes[row][column].value == 0:
            self.boxes[row][column].set_temp(0)

    def click(self, position):

        if position[0] < self.width and position[1] < self.height:
            spacing = self.width / 9
            row = position[0] // spacing
            column = position[1] // spacing
            return (int(column), int(row))
        else:
            return None

    def finished_board(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.boxes[i][j].value == 0:
                    return False
        return True


class Box:
    rows = 9
    columns = 9

    def __init__(self, value, row, column, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.column = column
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        font = pygame.font.SysFont("comicsans", 40)

        spacing = self.width/9
        column = self.column * spacing
        row = self.row * spacing

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (column+5, row+5))
        elif not self.value == 0:
            text = font.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (column + (spacing/2 - text.get_width()/2),
                            row + (spacing/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0),
                            (column, row, spacing, spacing), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y -
                                            2, self.width+4, self.height+4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y,
                                        self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 25)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

    def set_color(self, color):
        self.color = color


def reset_window(win, solve_button, verify_button, reset_puzzle_button, board, time, move):
    win.fill((255, 255, 255))
    font = pygame.font.SysFont("comicsans", 40)
    text = font.render(format_time(time), 1, (0, 0, 0))
    win.blit(text, (450, 545))
    text = font.render(str(move), 1, (0, 255, 0))
    win.blit(text, (20, 545))
    solve_button.draw(win)
    verify_button.draw(win)
    reset_puzzle_button.draw(win)
    board.draw(win)


def format_time(seconds):
    second = seconds % 60
    minute = seconds//60

    time = " " + str(minute) + ":" + str(second)
    return time


def main():
    window = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    sudoku_board = Grid(9, 9, 540, 540)
    solve_button = Button((0, 255, 0), 240, 545, 60, 25, text="Solve")
    verify_button = Button((0, 255, 0), 310, 545, 60, 25, text="Verify")
    reset_puzzle_button = Button((0, 255, 0), 380, 545, 60, 25, text="Reset")
    key = None
    run = True
    start = time.time()
    move = ""
    while run:

        elapsed_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    sudoku_board.clear_box()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = sudoku_board.selected
                    if sudoku_board.boxes[i][j].temp != 0:
                        if sudoku_board.make_move(sudoku_board.boxes[i][j].temp):
                            move = "Valid Move"
                        else:
                            move = "Invalid Move"
                        key = None

            if event.type == pygame.MOUSEMOTION:
                position = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                clicked = sudoku_board.click(position)
                if clicked:
                    sudoku_board.make_selection(clicked[0], clicked[1])
                    key = None
                if solve_button.isOver(position):
                    sudoku_board.solve_board()
                    sudoku_board.draw_solved_board(window)
                    move = "Finished Board!"
                if verify_button.isOver(position):
                    if verify_solution(sudoku_board.sudoku_board):
                        move = "Valid Solution"
                    else:
                        move = "Invalid Solution"
                if reset_puzzle_button.isOver(position):
                    sudoku_board = sudoku_board = Grid(9, 9, 540, 540)
                    move = ""
                    start = time.time()

            if sudoku_board.finished_board() and verify_solution(sudoku_board.sudoku_board):
                move = "Valid Solution"

        if sudoku_board.selected and key != None:
            sudoku_board.temp_draw(key)

        reset_window(window, solve_button, verify_button,
                    reset_puzzle_button, sudoku_board, elapsed_time, move)
        pygame.display.update()


main()
pygame.quit()
