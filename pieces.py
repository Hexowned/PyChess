import pygame
import os

black_pawn = pygame.image.load(os.path.join("img", "black_pawn.png"))
black_bishop = pygame.image.load(os.path.join("img", "black_bishop.png"))
black_knight = pygame.image.load(os.path.join("img", "black_knight.png"))
black_rook = pygame.image.load(os.path.join("img", "black_rook.png"))
black_king = pygame.image.load(os.path.join("img", "black_king.png"))
black_queen = pygame.image.load(os.path.join("img", "black_queen.png"))

white_pawn = pygame.image.load(os.path.join("img", "white_pawn.png"))
white_bishop = pygame.image.load(os.path.join("img", "white_bishop.png"))
white_knight = pygame.image.load(os.path.join("img", "white_knight.png"))
white_rook = pygame.image.load(os.path.join("img", "white_rook.png"))
white_king = pygame.image.load(os.path.join("img", "white_king.png"))
white_queen = pygame.image.load(os.path.join("img", "white_queen.png"))

black = [black_pawn, black_bishop, black_knight,
         black_rook, black_king, black_queen]
white = [white_pawn, white_bishop, white_knight,
         white_rook, white_king, white_queen]

BLACK = []
WHITE = []

for img in black:
    BLACK.append(pygame.transform.scale(img, (55, 55)))

for img in white:
    WHITE.append(pygame.transform.scale(img, (55, 55)))


class Piece:
    img = -1
    rect = (113, 113, 525, 525)
    startX = rect[0]
    startY = rect[1]

    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.selected = False
        self.move_list = []
        self.king = False
        self.pawn = False

    def is_selected(self):
        return self.selected

    def update_valid_moves(self, board):
        self.move_list = self.valid_moves(board)

    def draw(self, window, color):
        if self.color == "white":
            draw_this = WHITE[self.img]
        else:
            draw_this = BLACK[self.img]

        x = (4 - self.column) + round(self.startX +
                                      (self.column * self.rect[2] / 8))
        y = 3 + round(self.startY + (self.row * self.rect[3] / 8))

        if self.selected and self.color == color:
            pygame.draw.rect(window, (255, 0, 0), (x, y, 62, 62), 4)

        window.blit(draw_this, (x, y))

    def change_position(self, position):
        self.row = position[0]
        self.column = position[1]

    def __str__(self):
        return str(self.column) + " " + str(self.row)


class Pawn(Piece):
    img = 3

    def __init__(self, row, column, color):
        super().__init__(row, column, color)
        self.first = True
        self.queen = False
        self.pawn = True

    def valid_moves(self, board):
        i = self.row
        j = self.column

        moves = []
        try:
            if self.color == "black":
                if i < 7:
                    player = board[i + 1][j]
                    if player == 0:
                        moves.append((j, i + 1))

                    # DIAGONAL
                    if j < 7:
                        player = board[i + 1][j + 1]
                        if player != 0:
                            if player.color != self.color:
                                moves.append((j - 1, i + 1))

                if self.first:
                    if i < 6:
                        player = board[i + 2][j]
                        if player == 0:
                            if board[i + 1][j] == 0:
                                moves.append((j, i + 2))
                        elif player.color != self.color:
                            moves.append((j, i + 2))
            # WHITE
            else:
                if i > 0:
                    player = board[i - 1][j]
                    if player == 0:
                        moves.append((j, i - 1))

                if j < 7:
                    player = board[i - 1][j + 1]
                    if player != 0:
                        if player.color != self.color:
                            moves.append((j + 1, i - 1))

                if j > 0:
                    player = board[i - 1][j - 1]
                    if player != 0:
                        if player.color != self.color:
                            moves.append((j - 1, i - 1))

                if self.first:
                    if i > 1:
                        player = board[i - 2][j]
                        if player == 0:
                            if board[i - 1][j] == 0:
                                moves.append((j, 1 - 2))
                        elif player.color != self.color:
                            moves.append((j, 1 - 2))
        except:
            pass  # TODO: cannot use bare except, must return something..

        return moves


class Bishop(Piece):
    img = 0

    def valid_moves(self, board):
        i = self.row
        j = self.column

        moves = []

        # TOP RIGHT
        djL = j + 1
        djR = j - 1
        for di in range(i - 1, -1, -1):
            if djL < 8:
                player = board[di][djL]
                if player == 0:
                    moves.append((djL, di))
                elif player.color != self.color:
                    moves.append((djL, di))
                    break
                else:
                    break
            else:
                break

            djL += 1

        for di in range(i - 1, -1, -1):
            if djR > -1:
                player - board[di][djR]
                if player == 0:
                    moves.append((djR, di))
                elif player.color != self.color:
                    moves.append((djR, di))
                    break
                else:
                    break
            else:
                break

            djR -= 1

        # TOP LEFT
        djL = j + 1
        djR = j - 1
        for di in range(i + 1, 8):
            if djL < 8:
                player = board[di][djL]
                if player == 0:
                    moves.append((djL, di))
                elif player.color != self.color:
                    moves.append((djL, di))
                    break
                else:
                    break
            else:
                break

            djL += 1
        for di in range(i + 1, 8):
            if djR > -1:
                player - board[di][djR]
                if player == 0:
                    moves.append((djR, di))
                elif player.color != self.color:
                    moves.append((djR, di))
                    break
                else:
                    break
            else:
                break

            djR -= 1

        return moves


class Knight(Piece):
    img = 2

    def valid_moves(self, board):
        i = self.row
        j = self.column

        moves = []

        # DOWN LEFT
        if i < 6 and j > 0:
            player = board[i + 2][j - 1]
            if player == 0:
                moves.append((j - 1, i + 2))
            elif player.color != self.color:
                moves.append((j - 1, i + 2))

        # UP LEFT
        if i > 1 and j > 0:
            player = board[i - 2][j - 1]
            if player == 0:
                moves.append((j - 1, i - 2))
            elif player.color != self.color:
                moves.append((j - 1, i - 2))

        # DOWN RIGHT
        if i < 6 and j < 7:
            player = board[i + 2][j + 2]
            if player == 0:
                moves.append((j + 1, i + 2))
            elif player.color != self.color:
                moves.append((j + 1, i + 2))

        # UP RIGHT
        if i > 1 and j < 7:
            player = board[i - 2][j + 1]
            if player == 0:
                moves.append((j + 1, i - 2))
            elif player.color != self.color:
                moves.append((j + 1, i - 2))

        if i > 0 and j > 1:
            player = board[i - 1][j - 2]
            if player == 0:
                moves.append((j - 2, i - 1))
            elif player.color != self.color:
                moves.append((j - 2, i - 1))

        if i > 0 and j < 6:
            player = board[i - 1][j + 2]
            if player == 0:
                moves.append((j + 2, i - 1))
            elif player.color != self.color:
                moves.append((j + 2, i - 1))

        if i < 7 and j > 1:
            player = board[i + 1][j - 2]
            if player == 0:
                moves.append((j - 2, i + 1))
            elif player.color != self.color:
                moves.append((j - 2, i + 1))

        if i < 7 and j < 6:
            player = board[i + 1][j + 2]
            if player == 0:
                moves.append((j + 2, i + 1))
            elif player.color != self.color:
                moves.append((j + 2, i + 1))

        return moves


class Rook(Piece):
    img = 5

    def valid_moves(self, board):
        i = self.row
        j = self.column

        moves = []

        # UP
        for x in range(i - 1, -1, -1):
            player = board[x][j]
            if player == 0:
                moves.append((j, x))
            elif player.color != self.color:
                moves.append((j, x))
                break
            else:
                break

        # DOWN
        for x in range(i + 1, 8, 1):
            player = board[x][j]
            if player == 0:
                moves.append((j, x))
            elif player.color != self.color:
                moves.append((j, x))
                break
            else:
                break

        # LEFT
        for x in range(j - 1, -1, -1):
            player = board[i][x]
            if player == 0:
                moves.append((x, i))
            elif player.color != self.color:
                moves.append((x, i))
                break
            else:
                break

        # RIGHT
        for x in range(j + 1, 8, 1):
            player = board[i][x]
            if player == 0:
                moves.append((x, i))
            elif player.color != self.color:
                moves.append((x, i))
                break
            else:
                break

        return moves


class King(Piece):
    img = 1

    def __init__(self, row, column, color):
        super().__init__(row, column, color)
        self.king = True

    def valid_moves(self, board):
        i = self.row
        j = self.column

        moves = []

        if i > 0:
            # TOP LEFT
            if j > 0:
                player = board[i - 1][j - 1]
                if player == 0:
                    moves.append((j - 1, i - 1,))
                elif player.color != self.color:
                    moves.append((j - 1, i - 1,))

            # TOP MIDDLE
            player = board[i - 1][j]
            if player == 0:
                moves.append((j, i - 1))
            elif player.color != self.color:
                moves.append((j, i - 1))

            # TOP RIGHT
            if j < 7:
                player = board[i - 1][j + 1]
                if player == 0:
                    moves.append((j + 1, i - 1,))
                elif player.color != self.color:
                    moves.append((j + 1, i - 1,))

        if i < 7:
            # BOTTOM LEFT
            if j > 0:
                player = board[i + 1][j - 1]
                if player == 0:
                    moves.append((j - 1, i + 1,))
                elif player.color != self.color:
                    moves.append((j - 1, i + 1,))

            # BOTTOM MIDDLE
            player = board[i + 1][j]
            if player == 0:
                moves.append((j, i + 1))
            elif player.color != self.color:
                moves.append((j, i + 1))

            # BOTTOM RIGHT
            if j < 7:
                player = board[i + 1][j + 1]
                if player == 0:
                    moves.append((j + 1, i + 1))
                elif player.color != self.color:
                    moves.append((j + 1, i + 1))

        # MIDDLE LEFT
        if j > 0:
            player = board[i][j - 1]
            if player == 0:
                moves.append((j - 1, i))
            elif player.color != self.color:
                moves.append((j - 1, i))

        # MIDDLE RIGHT
        if j < 7:
            player = board[i][j + 1]
            if player == 0:
                moves.append((j + 1, i))
            elif player.color != self.color:
                moves.append((j + 1, i))

        return moves


class Queen(Piece):
    img = 4

    def valid_moves(self, board):
        i = self.row
        j = self.column

        moves = []

        # TOP RIGHT
        djL = j + 1
        djR = j - 1
        for di in range(i - 1, -1, -1):
            if djL < 8:
                player = board[di][djL]
                if player == 0:
                    moves.append((djL, di))
                elif player.color != self.color:
                    moves.append((djL, di))
                    break
                else:
                    djL = 9

            djL += 1

        for di in range(i - 1, -1, -1):
            if djR > -1:
                player = board[di][djR]
                if player == 0:
                    moves.append((djR, di))
                elif player.color != self.color:
                    moves.append((djR, di))
                    break
                else:
                    djR = -1

            djR -= 1

        # TOP LEFT
        djL = j + 1
        djR = j - 1
        for di in range(i + 1, 8):
            if djL < 8:
                player = board[di][djL]
                if player == 0:
                    moves.append((djL, di))
                elif player.color != self.color:
                    moves.append((djL, di))
                    break
                else:
                    djL = 9
            djL += 1

        for di in range(i + 1, 8):
            if djR > -1:
                player = board[di][djR]
                if player == 0:
                    moves.append((djR, di))
                elif player.color != self.color:
                    moves.append((djR, di))
                    break
                else:
                    djR = -1
            djR -= 1

        # UP
        for x in range(i - 1, -1, -1):
            player = board[x][j]
            if player == 0:
                moves.append((j, x))
            elif player.color != self.color:
                moves.append((j, x))
                break
            else:
                break

        # DOWN
        for x in range(i + 1, 8, 1):
            player = board[x][j]
            if player == 0:
                moves.append((j, x))
            elif player.color != self.color:
                moves.append((j, x))
                break
            else:
                break

        # LEFT
        for x in range(j - 1, -1, -1):
            player = board[i][x]
            if player == 0:
                moves.append((x, i))
            elif player.color != self.color:
                moves.append((x, i))
                break
            else:
                break

        # RIGHT
        for x in range(j + 1, 8, 1):
            player = board[i][x]
            if player == 0:
                moves.append((x, i))
            elif player.color != self.color:
                moves.append((x, i))
                break
            else:
                break

        return moves
