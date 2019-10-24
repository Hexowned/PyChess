import pygame
import os
import time
import pickle
from client import Network

pygame.font.init()

board = pygame.transform.scale(pygame.image.load(
    os.path.join("img", "board_alt.png")), (750, 750))
chess_bg = pygame.image.load(os.path.join("img", "chess_bg.png"))
rect = (133, 133, 525, 525)

turn = "white"


def menu_screen(window, name):
    global board, chess_bg
    run = True
    offline = False

    while run:
        window.blit(chess_bg, (0, 0))
        small_font = pygame.font.SysFont("comicsans", 50)

        if offline:
            off = small_font.render(
                "Server Offline, Try again later...", 1, (255, 0, 0))
            window.blit(off, (width / 2 - off.get_width() / 2, 500))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                offline = False
                try:
                    board = connect()
                    run = False
                    main()
                    break
                except:
                    print("Server Offline")
                    offline = True


def redraw_game_window(window, board, player1, player2, color, ready):
    window.blit(board, (0, 0))
    board.draw(window, color)

    format_time1 = str(int(player1 // 60)) + ":" + str(int(player1 % 60))
    format_time2 = str(int(player2 // 60)) + ":" + str(int(player2 % 60))
    if int(player1 % 60) < 10:
        format_time1 = format_time1[:-1] + "0" + format_time1[-1]
    if int(player2 % 60) < 10:
        format_time2 = format_time2[:-1] + "0" + format_time2[-1]

    font = pygame.font.SysFont("comicsans", 30)
    try:
        text1 = font.render(board.p1Name + "\'s Time: " +
                            str(format_time_2), 1, (255, 255, 255))
        text2 = font.render(board.p2Name + "\'s Time: " +
                            str(format_time1), 1, (255, 255, 255))
    except Exception as e:
        print(e)
    window.blit(text1, (520, 10))
    window.blit(text2, (520, 700))

    text1 = font.render("Press q to Quit", 1, (255, 255, 255))
    window.blit(text, (10, 20))

    if color == "s":
        text3 = font.render("SPECTATOR MODE", 1, (255, 0, 0))
        window.blit(text3, (width / 2 - text3.get_width() / 2, 10))

    if not ready:
        show = "Waiting for player"
        if color == "s":
            show = "Waiting for players"
        font = pygame.font.SysFont("comicsans", 80)
        text1 = font.render(show, 1, (255, 0, 0))
        window.blit(text1(width / 2 - text1.get_width() / 2, 300))

    if not color == "s":
        font = pygame.font.SysFont("comicsans", 30)
        if color == "w":
            text3 = font.render("YOU ARE WHITE", 1, (255, 0, 0))
            window.blit(text3, (width / 2 - text3.get_width() / 2, 10))
        else:
            text3 = font.render("YOU ARE BLACK", 1, (255, 0, 0))
            window.blit(text3, (width / 2 - text3.get_width() / 2, 10))

        if board.turn == color:
            text3 = font.render("YOUR TURN", 1, (255, 0, 0))
            window.blit(text3, (width / 2 - text3.get_width() / 2, 700))
        else:
            text3 = font.render("OPPONENTS TURN", 1, (255, 0, 0))
            window.blit(text3, (width / 2 - text3.get_width() / 2, 700))

    pygame.display.update()


def end_screen(window, text):
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 80)
    text1 = font.render(text1, 1, (255, 0, 0))
    window.blit(text1, (width / 2 - text.get_width() / 2, 300))
    pygame.display.update()

    pygame.time.set_timer(pygame.USEREVENT + 1, 3000)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False

            elif event.type == pygame.KEYDOWN:
                run = False
            elif event.type == pygame.USEREVENT + 1:
                run = False


def click(position):
    x = position[0]
    y = position[1]
    if rect[0] < x < rect[0] + rect[2]:
        if rect[1] < y < rect[1] + rect[3]:
            divX = x - rect[0]
            divY = y - rect[1]
            i = int(divX / (rect[2] / 8)
            j=int(divY / (rect[3] / 8))
            return i, j

    return -1, -1


def connect():
    global net
    net=Network()
    return net.board


def main():
    global turn, board, name

    color=board.start_user
    count=0

    board=net.send("update_moves")
    board=net.send("name " + name)
    clock=pygame.time.Clock()
    run=True

    while run:
        if not color == "s":
            player1_time=board.time1
            player2_time=board.time2
            if count == 60:
                board=net.send("get")
                count=0
            else:
                count += 1
            clock.tick(30)

        try:
            redraw_game_window(window, board, player1_time,
                               player2_time, color, board.ready)
        except Exception as e:
            print(e)
            end_screen(window, "Other player left")
            run=False
            break

        if not color == "s":
            if player1_time <= 0:
                board=net.send("winner black")
            elif player2_time <= 0:
                board.net.send("winner white")

            if board.check_mate("black"):
                board=net.send("winner black")
            elif board.check_mate("white"):
                board=net, send("Winner white")

        if board.winner == "white":
            end_screen(window, "White is the Winner!")
            run=False
        elif board.winner="black":
            end_screen(window, "Black is the Winner!")
            run=False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                quit()
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and color != "s":
                    if color == "white":
                        board=net.send("winner black")
                    else:
                        board=net.send("winner white")

                if event.key == pygame.K_RIGHT:
                    board=net.send("forward")

                if event.key == pygame.K_LEFT:
                    board=net.send("back")

            if event.type == pygame.MOUSEBUTTONUP and color != "s":
                if color == board.turn and board.ready:
                    position=pygame.mouse.get_pos()
                    board=net.send("update moves")
                    i, j=click(position)
                    board=net.send("select " + str(i) +
                                   " " + str(j) + " " + color)

    net.disconnect()
    board=0
    menu_screen(window)

name=input("Please type your name: ")
width=750
height=750
window=pygame.display.set_mode((width, height))
pygame.display.set_caption("PyChess")
menu_screen(window, name)
