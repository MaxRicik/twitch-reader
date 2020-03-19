import socket
import time
import json

with open("conf.json", "r") as soubor:

    conf = json.load(soubor)

sock = socket.socket()

server = 'irc.chat.twitch.tv'
port = 6667
welcome = False

sock.connect((server, port))

sock.send(f"PASS ".encode('utf-8') + conf["token"].encode('utf-8') + "\n".encode('utf-8'))
sock.send(f"NICK ".encode('utf-8') + conf["nickname"].encode('utf-8') + "\n".encode('utf-8'))
sock.send(f"JOIN #".encode('utf-8') + conf["channel"].encode('utf-8') + "\n".encode('utf-8'))

while True:

    raw_message = sock.recv(2048).decode('utf-8')

    if conf["debug"] == 1:

        print(raw_message)

    if raw_message == "":

        raise ValueError("You passed invalid arguments.")

    elif raw_message in ":tmi.twitch.tv NOTICE * :Login authentication failed\r\n":

        raise ValueError("Token is invalid.")
    
    if welcome == False:

        print("Program started successfully.")

        welcome = True

    if "JOIN" in raw_message.split():

        print(f"Program joined to channel {raw_message.split()[2]} successfully.")

    if raw_message.startswith('PING'):
        sock.send("PONG\n".encode('utf-8'))

    if "PRIVMSG" in raw_message:

        poc = 0
        list_message = list()
        message = str()

        for i in raw_message:

            if poc == 2:

                list_message += i

            elif i == ":":

                poc += 1

        for i in range(len(list_message) - 2):

            message += list_message[i]

        # vars: message, raw_message (raw output from Twitch API)
        # začátek kódu
        
        if "#dotaz" in message.split():

            with open("dotazy.txt", "a+", encoding="utf-8") as soubor:

                soubor.write(message + "\n")

        # konec kódu

        if conf["output"] == 1:

            print(message)