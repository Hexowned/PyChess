import pygame
import time
from pieces import Pawn
from pieces import Bishop
from pieces import Knight
from pieces import Rook
from pieces import King
from pieces import Queen


class Board:
    rect = (113, 113, 525, 525)
    startX = rect[0]
    startY = rect[1]

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.ready = False
        self.last = None
        self.copy = True

        self.board = [[0 for x in range(8)] for _ in range(rows)]

        self.board[0][0] = Rook(0, 0, "black")
        self.board[0][1] = Knight(0, 1, "black")
        self.board[0][2] = Bishop(0, 2, "black")
        self.board[0][3] = Queen(0, 3, "blackwhite")
        self.board[0][4] = King(0, 4, "black")
        self.board[0][5] = Bishop(0, 5, "black")
        self.board[0][6] = Knight(0, 6, "black")
        self.board[0][7] = Rook(0, 7, "black")

        self.board[1][0] = Pawn(1, 0, "black")
        self.board[1][1] = Pawn(1, 1, "black")
        self.board[1][2] = Pawn(1, 2, "black")
        self.board[1][3] = Pawn(1, 3, "black")
        self.board[1][4] = Pawn(1, 4, "black")
        self.board[1][5] = Pawn(1, 5, "black")
        self.board[1][6] = Pawn(1, 6, "black")
        self.board[1][7] = Pawn(1, 7, "black")

        self.board[7][0] = Rook(7, 0, "white")
        self.board[7][1] = Knight(7, 1, "white")
        self.board[7][2] = Bishop(7, 2, "white")
        self.board[7][3] = Queen(7, 3, "white")
        self.board[7][4] = King(7, 4, "white")
        self.board[7][5] = Bishop(7, 5, "white")
        self.board[7][6] = Knight(7, 6, "white")
        self.board[7][7] = Rook(7, 7, "white")

        self.board[6][0] = Pawn(6, 0, "white")
        self.board[6][1] = Pawn(6, 1, "white")
        self.board[6][2] = Pawn(6, 2, "white")
        self.board[6][3] = Pawn(6, 3, "white")
        self.board[6][4] = Pawn(6, 4, "white")
        self.board[6][5] = Pawn(6, 5, "white")
        self.board[6][6] = Pawn(6, 6, "white")
        self.board[6][7] = Pawn(6, 7, "white")

        self.p1Name = "Player 1"
        self.p2Name = "Player 2"
        self.turn = "white"

        self.time1 = 900
        self.time2 = 900
        self.storedTime1 = 0
        self.storedTime2 = 0

        self.winner = None
        self.startTime = time.time()

    def update_moves(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    self.board[i][j].update_valid_moves(self.board)

    def draw(self, window, color):
        if self.last and color == self.turn:
            y, x = self.last[0]
            y1, x1 = self.last[1]

            xx = (4 - x) + round(self.startX + (x * self.rect[2] / 8))
            yy = 3 + round(self.startY + (y * self.rect[3] / 8))
            pygame.draw.circle(window, (0, 0, 255),
                               (xx + 32, yy + 30), 34, 4)

            xx1 = (4 - x) + round(self.startX + (x1 * self.rect[2] / 8))
            yy1 = 3 + round(self.startY + (y1 * self.rect[3] / 8))
            pygame.draw.cirlce(window, (0, 0, 255),
                               (xx1 + 32, yy1 + 30), 34, 4)

        s = None
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    self.board[i][j].draw(window, color)
                    if self.board[i][j].is_selected:
                        s = (i, j)
