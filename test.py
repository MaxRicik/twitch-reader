import tkinter as tk
from tkinter import scrolledtext
import time
import os
import socket
import json
from threading import Thread

def frontend():

    root = tk.Tk()

    def refresh():

        with open("dotazy.txt", "r", encoding="utf-8") as soubor:

            okenko.delete(1.0, tk.END)
            okenko.insert(tk.END, soubor.read())
        
        root.after(conf["refresh-rate"], refresh)

    def delt():

        os.system("del dotazy.txt")
        
        with open("dotazy.txt", "w"):

            pass

    def nast():

        pass

    with open("conf.json", "r") as soubor:

        conf = json.load(soubor)

    okenko = scrolledtext.ScrolledText(root)
    okenko.grid(row=0, column=0, columnspan=2)

    btn = tk.Button(root, text="Refresh", command=refresh)
    btn.grid(row=1, column=0)

    rem = tk.Button(root, text="Clear", command=delt)
    rem.grid(row=1, column=1)

    """
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Nastavení", command=nast)
    root.config(menu=menu)
    """

    with open("dotazy.txt", "r", encoding="utf-8") as soubor:

        okenko.insert(tk.END, soubor.read())

    refresh()

    root.mainloop()

def backend():

    with open("conf.json", "r") as soubor:

        conf = json.load(soubor)

    sock = socket.socket()

    server = 'irc.chat.twitch.tv'
    port = 6667
    welcome = False
    fe_stav = False
    correct_run = False

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

            print("Program started successfully.\nCan't connect to the channel chat.", end="\r")

            welcome = True

        elif "JOIN" in raw_message.split():

            print(f"Program joined to channel {raw_message.split()[2]} successfully.")

            correct_run = True

        if correct_run == True and fe_stav == False:

            Thread(target=frontend).start()

            fe_stav = True

        if raw_message.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))

        if "PRIVMSG" in raw_message:

            poc = 0
            list_message = list()
            message = str()
            s = 1
            k = int()

            for i in range(len(raw_message)):

                if raw_message[i] == "!":

                    k = i
                    break


            nick = raw_message[1:k]

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

                    soubor.write(f"{nick}: {message}\n")

            if "#review" in message.split():

                with open("review.txt", "a+", encoding="utf-8") as soubor:

                    soubor.write(f"{nick}: {message}")

            # konec kódu

            if conf["output"] == 1:

                print(nick, message)

Thread(target=backend).start()