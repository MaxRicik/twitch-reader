import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import os
import socket
import json
from threading import Thread

def frontend():

    class App:

        def __init__(self):

            with open("conf.json", "r") as soubor:

                self.conf = json.load(soubor)

            self.root = tk.Tk()
            self.root.bind("<Delete>", self.delt)
            self.root.bind("<Up>", self.up)
            self.root.bind("<Down>", self.down)
            self.root.bind("<r>", self.refresh)

            self.commands_om_var = tk.StringVar()
            self.commands_om_var.set(self.conf["commands"][0])
            self.commands_om = tk.OptionMenu(self.root, self.commands_om_var, *self.conf["commands"], command=self.refresh)
            self.commands_om.grid(row=0, column=0)

            self.okenko = scrolledtext.ScrolledText(self.root)
            self.okenko.grid(row=1, column=0, columnspan=2, sticky="wen")

            self.btn = tk.Button(self.root, text="Refresh", command=self.refresh)
            self.btn.grid(row=2, column=0)

            self.rem = tk.Button(self.root, text="Clear", command=self.delt)
            self.rem.grid(row=2, column=1)

            self.refresh()

            self.root.mainloop()

        def refresh(self, var=str()):

            try:

                with open(f"{self.commands_om_var.get()}.txt", "r", encoding="utf-8") as soubor:

                    self.okenko.delete(1.0, tk.END)
                    self.okenko.insert(tk.END, soubor.read())

            except FileNotFoundError:

                with open(f"{self.commands_om_var.get()}.txt", "w"):

                    pass

            poc = 0

            for i in self.conf["commands"]:

                if i == self.commands_om_var.get():

                    self.commands_om_var_now = poc

                poc += 1

            self.okenko.yview_moveto(1.0)

            self.root.after(self.conf["refresh-rate"], self.refresh)

        def delt(self, event):

            choice = messagebox.askyesno("Twitch reader", f"Do you really want to delete {self.commands_om_var.get()}.txt?")

            if choice == True:

                os.system(f"del {self.commands_om_var.get()}.txt")
                
                with open(f"{self.commands_om_var.get()}.txt", "w") as soubor:

                    self.okenko.delete(1.0, tk.END)

        def up(self, event):

            if self.commands_om_var_now > 0:

                self.commands_om_var.set(self.conf["commands"][self.commands_om_var_now - 1])

                self.refresh()

        def down(self, event):

            if self.commands_om_var_now + 1 < len(self.conf["commands"]):

                self.commands_om_var.set(self.conf["commands"][self.commands_om_var_now + 1])

                self.refresh()

    app = App()

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

        if conf["raw_output"] == 1:

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

        if correct_run == True and fe_stav == False and conf["gui"] == 1:

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

            # znickname get

            for i in range(len(raw_message)):

                if raw_message[i] == "!":

                    k = i
                    break


            nick = raw_message[1:k]

            # message convert to list form

            for i in raw_message:

                if poc == 2:

                    list_message += i

                elif i == ":":

                    poc += 1
            
            # converting mention to non-conflict format

            for i in range(len(list_message) - 2):

                message += list_message[i]

            message_split = message.split()

            for i in range(len(message_split)):

                if message_split[i].startswith("@") == True:

                    message_split[i] = message_split[i].lower()

            message = str()

            # message convert to string form

            for i in range(len(message_split)):

                message += message_split[i] + " "

            # vars: message, raw_message (raw output from Twitch API), nick
            # začátek kódu

            for i in conf["commands"]:
            
                    if f"{i}" in message.split():

                        with open(f"{i}.txt", "a+", encoding="utf-8") as soubor:

                            soubor.write(f"{nick}: {message}\n")

            # konec kódu

            if conf["output"] == 1:

                print(nick, message)

Thread(target=backend).start()