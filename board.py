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

    def get_danger_moves(self, color):
        danger_moves = []
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    if self.board[i][j].color != color:
                        for move in self.board[i][j].move_list:
                            danger_moves.append(move)

        return danger_moves

    def is_checked(self, color):
        self.update_moves()
        danger_moves = self.get_danger_moves(color)
        king_position = (-1, -1)
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    if self.board[i][j].king and self.board[i][j].color == color:  # noqa E501
                        king_position = (j, i)

        if king_position in danger_moves:
            return True

        return False

    def select(self, column, row, color):
        changed = False
        previous = (-1, -1)
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    if self.board[i][j] != 0:
                        if self.board[i][j].selected:
                            previous = (i, j)

        if self.board[row][column] == 0 and previous != (-1, -1):
            moves = self.board[previous[0]][previous[1]].move_list
            if (column, row) in moves:
                changed = self.move(previous, (row, column), color)
        else:
            if previous == (-1, -1):
                self.reset_selected()
                if self.board[row][column] != 0:
                    self.board[row][column].selected = True
            else:
                if self.board[previous[0]][previous[1]].color != self.board[row][column].color:  # noqa E501
                    moves = self.board[previous[0]][previous[1]].move_list
                    if (column, row) in moves:
                        changed = self.move(previous, (row, column), color)

                    if self.board[row][column].color == color:
                        self.board[row][column].selected = True
                else:
                    if self.board[row][column].color == color:
                        # castle-ing
                        self.reset_selected()
                        if self.board[previous[0]][previous[1]].moved == False and self.board[previous[0]][previous[1]].rook and self.board[row][column].king and column != previous[1] and previous != (-1, -1):  # noqa E501
                            castle = True
                            if previous[1] < column:
                                for j in range(previous[1] + 1, column):
                                    if self.board[row][j] != 0:
                                        castle = False

                                if castle:
                                    changed = self.move(
                                        previous, (row, 3), color)
                                    changed = self.move(
                                        (row, column), (row, 2), color)
                                if not changed:
                                    self.board[row][column].selected = True
                            else:
                                for j in range(column + 1, previous[1]):
                                    if self.board[row][j] != 0:
                                        castle = False

                                if castle:
                                    changed = self.move(
                                        previous, (row, 6), color)
                                    changed = self.move(
                                        (row, column), (row, 5), color)
                                if not changed:
                                    self.board[row][column].selected = True
                        else:
                            self.board[row][column].selected = True
        if changed:
            if self.turn == "white":
                self.turn = "black"
                self.reset_selected()
            else:
                self.turn = "white"
                self.reset_selected()

    def reset_selected(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    self.board[i][j].selected = False

    def check_mate(self, color):
        pass  # TODO: need to implement this correctly

    def move(self, start, end, color):
        checkedBefore = self.is_checked(color)
        changed = True
        nBoard = self.board[:]
        if nBoard[start[0]][start[1]].pawn:
            nBoard[start[0]][start[1]].first = False

        nBoard[start[0]][start[1]].change_pos((end[0], end[1]))
        nBoard[end[0]][end[1]] = nBoard[start[0]][start[1]]
        nBoard[start[0]][start[1]] = 0
        self.board = nBoard

        if self.is_checked(color) or (checkedBefore and self.is_checked(color)):  # noqa E501
            changed = False
            nBoard = self.board[:]
            nBoard = self.board[:]
            if nBoard[end[0]][end[1]].pawn:
                nBoard[end[0]][end[1]].first = True

            nBoard[end[0]][end[1]].change_pos((start[0], start[1]))
            nBoard[start[0]][start[1]] = nBoard[end[0]][end[1]]
            nBoard[end[0]][end[1]] = 0
            self.board = nBoard
        else:
            self.reset_selected()

        self.update_moves()
        if changed:
            self.last = [start, end]
            if self.turn == "white":
                self.storedTime1 += (time.time() - self.startTime)
            else:
                self.storedTime2 += (time.time() - self.startTime)
            self.startTime = time.time()

        return changed
