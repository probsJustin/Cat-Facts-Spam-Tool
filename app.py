import requests
import tkinter as tk
from functools import partial
from twilio.rest import Client
import os
from api import account_sid, auth_token
import threading

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
        self.buttons["send"].grid(row=1, column=0, padx=20, pady=20)
        self.buttons["send"]["text"] = "send"

        self.buttons["reset"] = tk.Button(self, borderwidth=10, command=partial(self.actions, "reset"))
        self.buttons["reset"].grid(row=1, column=1, padx=20, pady=20)
        self.buttons["reset"]["text"] = "reset"

        self.fields["phone_number"] = tk.Text(self, height=2, width=40)
        self.fields["phone_number"].grid(row=0, column=1, columnspan=3, padx=20, pady=20)

        self.fields["amount_loop"] = tk.Text(self, height=2, width=10)
        self.fields["amount_loop"].grid(row=3, column=1, padx=20, pady=20)

        self.labels["phone_number"] = tk.Label(self, borderwidth=10)
        self.labels["phone_number"].grid(row=0, column=0, padx=20, pady=20)
        self.labels["phone_number"]["text"] = "Phone Number"

        self.labels["amount_loop"] = tk.Label(self, borderwidth=20)
        self.labels["amount_loop"].grid(row=3, column=0, padx=20, pady=20)
        self.labels["amount_loop"]["text"] = "# of cat facts"

    def threaded_sms_loop(self):
        if (self.fields["amount_loop"].get("1.0", tk.END) == ""):
            print(type(self.fields["phone_number"].get("1.0", tk.END)))
            self.create_sms(self.get_cat_facts(), str(self.fields["phone_number"].get("1.0", tk.END)))

        else:
            counter = int(self.fields["amount_loop"].get("1.0", tk.END))
            for x in range(0, counter):
                try:
                    print(type(self.fields["phone_number"].get("1.0", tk.END)))
                    self.create_sms(self.get_cat_facts(), str(self.fields["phone_number"].get("1.0", tk.END)))
                except Exception as e:
                    print(e)


    def actions(self, action):
        return_variable = action
        counter = 1
        if(action == "send"):
            sms_loop = threading.Thread(name='threaded_sms_loop', target=self.threaded_sms_loop)
            sms_loop.start()

        if (action == "reset"):
            print(self.get_cat_facts())


    def create_sms(self, text, phone_number):
        from twilio.rest import Client

        # Your Account Sid and Auth Token from twilio.com/console
        # and set the environment variables. See http://twil.io/secure

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body = text,
            from_= '+16143680119',
            to = phone_number
        )



    def get_cat_facts(self):
        return requests.get(url="https://catfact.ninja/fact").json()["fact"]


root = tk.Tk(className="Cat Facts")
root.geometry("600x400")
app = gui_stuff(master=root)
app.mainloop()




