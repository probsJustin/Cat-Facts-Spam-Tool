import requests
import tkinter as tk
from functools import partial
import os
from api import account_sid, auth_token
import threading
import random
import time

class gui_stuff(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.buttons = dict()
        self.labels = dict()
        self.fields = dict()
        self.master = master
        self.pack()
        self.init_ui()

    def init_ui(self):
        self.buttons["send"] = tk.Button(self, borderwidth=10, command=partial(self.actions, "send"))
        self.buttons["send"].grid(row=3, column=0, padx=1, pady=1)
        self.buttons["send"]["text"] = "send"

        self.buttons["reset"] = tk.Button(self, borderwidth=10, command=partial(self.actions, "reset"))
        self.buttons["reset"].grid(row=3, column=1, padx=1, pady=1)
        self.buttons["reset"]["text"] = "reset"

        self.buttons["random"] = tk.Button(self, borderwidth=10, command=partial(self.actions, "random"))
        self.buttons["random"].grid(row=3, column=4, padx=1, pady=1)
        self.buttons["random"]["text"] = "random"

        self.buttons["new_window"] = tk.Button(self, borderwidth=10, command=partial(self.actions, "new_window"))
        self.buttons["new_window"].grid(row=3, column=2, padx=1, pady=1)
        self.buttons["new_window"]["text"] = "new window"

        self.fields["phone_number"] = tk.Text(self, height=1, width=40)
        self.fields["phone_number"].grid(row=0, column=1, columnspan=4, padx=1, pady=1, sticky='w')

        self.fields["delay"] = tk.Text(self, height=1, width=15)
        self.fields["delay"].grid(row=2, column=3, columnspan=3, padx=1, pady=1, sticky='w')

        self.fields["amount_loop"] = tk.Text(self, height=1, width=10)
        self.fields["amount_loop"].grid(row=2, column=1, padx=1, pady=1, sticky='w')

        self.labels["phone_number"] = tk.Label(self, borderwidth=10)
        self.labels["phone_number"].grid(row=0, column=0, padx=1, pady=1, sticky='w')
        self.labels["phone_number"]["text"] = "Phone Number"

        self.labels["amount_loop"] = tk.Label(self, borderwidth=10)
        self.labels["amount_loop"].grid(row=2, column=0, padx=1, pady=1, sticky='w')
        self.labels["amount_loop"]["text"] = "# of cat facts"

        self.labels["delay"] = tk.Label(self, borderwidth=10)
        self.labels["delay"].grid(row=2, column=2, padx=1, pady=1, sticky='w')
        self.labels["delay"]["text"] = "Delay(seconds):"

    def threaded_sms_loop(self):
        if (self.fields["amount_loop"].get("1.0", tk.END) == ""):
            self.create_sms(self.get_cat_facts(), str(self.fields["phone_number"].get("1.0", tk.END)))
        else:
            try:
                counter = int(self.fields["amount_loop"].get("1.0", tk.END))
            except Exception as e:
                counter = 0
            for x in range(0, counter):
                try:
                    self.create_sms(self.get_cat_facts(), str(self.fields["phone_number"].get("1.0", tk.END)))
                except Exception as e:
                    print(e)



    def threaded_sms_random_loop(self):
        if (self.fields["amount_loop"].get("1.0", tk.END) == ""):
            self.create_sms(self.get_cat_facts(), str(self.fields["phone_number"].get("1.0", tk.END)))
        else:
            try:
                counter = int(self.fields["amount_loop"].get("1.0", tk.END))
            except Exception as e:
                counter = 0

            for x in range(0, counter):
                try:
                    time.sleep(random.randint(0, 5))
                    self.create_sms(self.get_cat_facts(), str(self.fields["phone_number"].get("1.0", tk.END)))
                except Exception as e:
                    print(e)

    def reset_fields(self):
        self.fields["phone_number"].delete("1.0", tk.END)
        self.fields["amount_loop"].delete("1.0", tk.END)


    def actions(self, action):
        return_variable = action
        if(action == "send"):
            if (self.fields["amount_loop"].get("1.0", tk.END) == '\n'):
                print("[warning] You left the loop amount empty we will assume 1")

            if(self.fields["phone_number"].get("1.0", tk.END) == '\n'):
                print("[severe] You left the phone number empty")
            else:
                sms_loop = threading.Thread(name='threaded_sms_loop', target=self.threaded_sms_loop)
                sms_loop.start()
                self.master.title("Cat Facts Low Orbiting Ion Cannon - Pew Pew Pew")

        if (action == "reset"):
            clear_fields = threading.Thread(name='threaded_sms_loop', target=self.reset_fields)
            clear_fields.start()


        if(action == "new_window"):
            self.create_new_window()

        if(action == "random"):
            if (self.fields["amount_loop"].get("1.0", tk.END) == '\n'):
                print("[warning] You left the loop amount empty we will assume 1")

            if(self.fields["phone_number"].get("1.0", tk.END) == '\n'):
                print("[severe] You left the phone number empty")
            else:
                sms_loop = threading.Thread(name='threaded_sms_loop', target=self.threaded_sms_random_loop)
                sms_loop.start()

    def create_new_window(self):
        newWindow = tk.Toplevel(self.master)
        newWindow.title("New Cat Facts Window Example")
        newWindow.geometry('200x200')
        tk.Label(newWindow, text="This is a new window").pack()

    def create_sms(self, text, phone_number):
        from twilio.rest import Client

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body = text,
            from_= '+16143680119',
            to = phone_number
        )

    def get_cat_facts(self):
        print("Cat Facts Cannon Ready: Pew....")
        return requests.get(url="https://catfact.ninja/fact").json()["fact"]

root = tk.Tk(className="Cat Facts")
root.title("Cat Facts Low Orbiting Ion Cannon")
root.geometry("500x150")
app = gui_stuff(master=root)
app.mainloop()





