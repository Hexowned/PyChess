import socket  # noqa E902
from _thread import *
from board import Board
import pickle
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "localhost"
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen()
print("[START] Waiting for a connection")

connections = 0

games = {0: Board(8, 8)}

spectator_ids = []
specs = 0


def read_specs():
    global spectator_ids

    spectator_ids = []
    try:
        with open("specs.txt", "r") as f:
            for line in f:
                spectator_ids.append(line.strip())
    except:  # noqa E722
        print("[ERROR] No specs.txt file found, creating one...")
        open("specs.txt", "")


def threaded_client(connection, game, spec=False):
    global position, games, currentId, connections, specs

    if not spec:
        name = None
        board = [game]

        if connections % 2 == 0:
            currentId = "white"
        else:
            currentId = "black"

        bo.start_user = currentId

        # Pickle the object and sent it to the server
        data_string = pickle.dumps(board)

        if currentId == "black":
            board.ready = True
            board.start_time = time.time()

        connection.send(data_string)
        connections += 1

        while True:
            if game not in game:
                break

            try:
                d = connection.recv(8129 * 3)
                data = d.decode("utf-8")
                if not d:
                    break
                else:
                    if data.count("select") > 0:
                        all = data.split(" ")
                        column = int(all[1])
                        row = int(all[2])
                        color = all[3]
                        board.select(column, row, color)

                    if data == "winner black":
                        board.winner = "black"
                        print("[GAME] Player black won in game", game)
                    if data == "winner white":
                        board.winner = "white"
                        print("[GAME] Player white won in game", game)

                    if data == "update moves":
                        board.update_moves()

                    if data.count("name") == 1:
                        name = data.split(" ")[1]
                        if currentId == "black":
                            board.player2_name = name
                        elif currentId == "white":
                            board.player1_name = name

                    if board.ready:
                        if board.turn == "white":
                            board.time1 = 900 - (time.time()) - board.start_time - board.stored_time1  # noqa E501
                        else:
                            board.time2 = 900 - (time.time()) - board.start_time - board.stored_time2  # noqa E501

                    send_data = pickle.dumps(board)

                connection.sendall(send_data)
            except Exception as e:
                print(e)

        connections -= 1
        try:
            del games[game]
            print("[GAME] Game", game, "ended")
        except:  # noqa E722
            pass
        print("[DISCONNECT] Player" name, "left game", game)
        connection.close()
    else:
        available_games = list(games.keys())
        game_ind = 0
        board = games[available_games[game_ind]]
        board.start_user = "start"
        data_string = pickle.dumps(board)
        connection.send(data_string)

        while True:
            available_games = list(games.keys())
            board = games[available_games[game]]
            try:
                d = connection.recv(128)
                data = d.decode("utf-8")
                if not d:
                    break
                else:
                    try:
                        if data == "forward"
                        print("SPECTATOR] Moves Games forward")
                        game_ind += 1
                        if game_ind >= len(available_games):
                            game_ind = 0
                    elif data == "back":
                        print("[SPECTATOR] Moves Games back")
                        game_ind -= 1
                        if game_ind < 0:
                            game_ind = len(available_games) - 1

                    board = games[available_games[game_ind]]
                except:  # noqa E722
                    print("[ERROR] Invalid game recieved from spectator")

                send_data = pickle.dumps(board)
                connection.sendall(send_data)
        except Exception as e:
            print(e)

    print("[DISCONNECT] Spectator left game", game)
    specs -= 1
    connection.close()


while True:
    read_specs()
    if connections < 6:
        connection, address = s.accept()
        spec = False
        g = -1
        print("[CONNECT] New connection")

        for game in games.keys():
            if games[game].ready = False:
                g = game

        if g == -1:
            try:
                g = list(games.keys())[-1] + 1
                games[g] = Board(8, 8)
                except:  # noqa E722
                    g = 0
                    games[g] = Board(8, 8)

        print("[DATA] Number of connections:", connections + 1)
        print("[DATA] Number of games:", len(games))
        start_new_thread(threaded_client, (connection, g, spec))
