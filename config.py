import tkinter as tk
from tkinter import messagebox
import json

class App:

    def __init__(self):

        with open("conf.json", "r", encoding="utf-8") as soubor:

            self.conf = json.load(soubor)

        self.root = tk.Tk()

        self.token_l = tk.Label(self.root, text="Token:", anchor="w", width=10)
        self.token_l.grid(row=0, column=0)
        self.token_e = tk.Entry(self.root, width=36)
        self.token_e.grid(row=0, column=1, columnspan=2)
        self.token_e.insert(tk.END, self.conf["token"])

        self.nick_l = tk.Label(self.root, text="Nick:", anchor="w", width=10)
        self.nick_l.grid(row=1, column=0)
        self.nick_e = tk.Entry(self.root, width=36)
        self.nick_e.grid(row=1, column=1, columnspan=2)
        self.nick_e.insert(tk.END, self.conf["nickname"])

        self.kanal_l = tk.Label(self.root, text="Channel:", anchor="w", width=10)
        self.kanal_l.grid(row=2, column=0)
        self.kanal_e = tk.Entry(self.root, width=36)
        self.kanal_e.grid(row=2, column=1, columnspan=2)
        self.kanal_e.insert(tk.END, self.conf["channel"])

        self.raw_output_var = tk.IntVar()
        self.raw_output_var.set(self.conf["raw_output"])
        self.raw_output_l = tk.Label(self.root, text="Raw output", anchor="w", width=10)
        self.raw_output_l.grid(row=3, column=0)
        self.raw_output_ch = tk.Checkbutton(self.root, variable=self.raw_output_var, command=self.test)
        self.raw_output_ch.grid(row=3, column=1, sticky="w", columnspan=2)

        self.output_var = tk.IntVar()
        self.output_var.set(self.conf["output"])
        self.output_l = tk.Label(self.root, text="Output", anchor="w", width=10)
        self.output_l.grid(row=4, column=0)
        self.output_ch = tk.Checkbutton(self.root, variable=self.output_var, command=self.test)
        self.output_ch.grid(row=4, column=1, sticky="w", columnspan=2)

        self.refresh_rate_l = tk.Label(self.root, text="Refresh rate: ", anchor="w", width=10)
        self.refresh_rate_l.grid(row=5, column=0)
        self.refresh_rate_e = tk.Entry(self.root, width=36)
        self.refresh_rate_e.grid(row=5, column=1, columnspan=2)
        self.refresh_rate_e.insert(tk.END, self.conf["refresh-rate"])

        self.commands_var_list = self.conf["commands"]
        self.commands_var_list.insert(0, "-Add-")
        self.commands_var = tk.StringVar()
        self.commands_var.set(self.commands_var_list[0])
        self.commands_om = tk.OptionMenu(self.root, self.commands_var, *self.conf["commands"], command=self.om_update)
        self.commands_om.grid(row=6, column=0)
        self.commands_om_add = tk.Entry(self.root)
        self.commands_om_add.grid(row=6, column=1, columnspan=2)
        self.commands_om_add_btn = tk.Button(self.root, text="Add", command=self.add)
        self.commands_om_add_btn.grid(row=6, column=2, columnspan=2)

        self.gui_var = tk.IntVar()
        self.gui_var.set(self.conf["gui"])
        self.gui_l = tk.Label(self.root, text="GUI", anchor="w", width=10)
        self.gui_l.grid(row=7, column=0)
        self.gui_ch = tk.Checkbutton(self.root, variable=self.gui_var, command=self.test)
        self.gui_ch.grid(row=7, column=1, sticky="w")

        self.commands_om_del_stav = False
        self.commands_om_add_stav = True

        self.root.protocol("WM_DELETE_WINDOW", self.apply)
        self.root.mainloop()

    def test(self):

        #print("s")
        pass


    def om_update(self, var):

        if self.commands_var.get() == "-Add-" and self.commands_om_add_stav == False:

            self.commands_om_del.grid_forget()

            self.commands_om_add = tk.Entry(self.root)
            self.commands_om_add.grid(row=6, column=1, columnspan=2)
            self.commands_om_add_btn = tk.Button(self.root, text="Add", command=self.add)
            self.commands_om_add_btn.grid(row=6, column=2, columnspan=2)

            self.commands_om_add_stav = True
            self.commands_om_del_stav = False

            


        elif self.commands_var.get() != "-Add-" and self.commands_om_del_stav == False:

            self.commands_om_add.grid_forget()
            self.commands_om_add_btn.grid_forget()

            self.commands_om_del = tk.Button(self.root, text="Remove", command=self.remove)
            self.commands_om_del.grid(row=6, column=1)

            self.commands_om_del_stav = True
            self.commands_om_add_stav = False

    def add(self):

        if len(self.commands_om_add.get()) == 0:

            messagebox.showerror("Config", "You didn't enter any data.")

            return

        elif self.commands_om_add.get() in self.conf["commands"]:

            messagebox.showerror("Config", "You entered existing hashtag.")

            return

        self.conf["commands"].append(self.commands_om_add.get())
        self.commands_om.grid_forget()

        self.commands_om = tk.OptionMenu(self.root, self.commands_var, *self.conf["commands"], command=self.om_update)
        self.commands_om.grid(row=6, column=0)

        messagebox.showinfo("Config", "Command was added.")

    def remove(self):

        messagebox.showinfo("Config", f"Hashtag {self.commands_var.get()} has been removed.")

        self.conf["commands"].remove(self.commands_var.get())

        self.commands_om.grid_forget()

        self.commands_om = tk.OptionMenu(self.root, self.commands_var, *self.conf["commands"], command=self.om_update)
        self.commands_om.grid(row=6, column=0)

        self.commands_var.set(self.conf["commands"][0])

        self.commands_om_del.grid_forget()

        self.commands_om_add = tk.Entry(self.root)
        self.commands_om_add.grid(row=6, column=1, columnspan=2)
        self.commands_om_add_btn = tk.Button(self.root, text="Add", command=self.add)
        self.commands_om_add_btn.grid(row=6, column=2, columnspan=2)

    def apply(self):

        choice = messagebox.askyesnocancel("Config", "Do you want to save data?")

        if choice == True:

            error = str()

            self.conf["token"] = self.token_e.get()

            if len(self.token_e.get()) != 36:

                error += "You entered invalid token.\n"

            self.conf["nickname"] = self.nick_e.get()
            self.conf["channel"] = self.kanal_e.get()
            self.conf["raw_output"] = self.raw_output_var.get()
            self.conf["output"] = self.output_var.get()

            try:

                int(self.refresh_rate_e.get())

            except ValueError:

                error += "You didn't entered a number in \"Refresh rate\".\n"

            else:

                self.conf["refresh-rate"] = self.refresh_rate_e.get()

            self.commands_var_list.remove("-Add-")

            self.conf["gui"] = self.gui_var.get()

            with open("conf.json", "w+") as soubor:

                soubor.write(json.dumps(self.conf))

            if len(error) == 0:

                self.root.destroy()

            else:

                messagebox.showerror("Config", f"Data can't be saved, because:\n{error}")

        if choice == False:

            self.root.destroy()

        if choice == None:

            pass

app = App()