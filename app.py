import requests
import tkinter as tk
from functools import partial
from twilio.rest import Client
import os

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

        self.labels["phone_number"] = tk.Label(self, borderwidth=10)
        self.labels["phone_number"].grid(row=0, column=0, padx=20, pady=20)
        self.labels["phone_number"]["text"] = "Phone Number"

    def actions(self, action):
        return_variable = action
        if(action == "send"):
            print(type(self.fields["phone_number"].get("1.0", tk.END)))
            self.create_sms(self.get_cat_facts(), str(self.fields["phone_number"].get("1.0", tk.END)))

        if (action == "reset"):
            print(self.get_cat_facts())


    def create_sms(self, text, phone_number):
        from twilio.rest import Client

        # Your Account Sid and Auth Token from twilio.com/console
        # and set the environment variables. See http://twil.io/secure
        account_sid = "AC1e09ea82c62ff5d844472d65bf8a4e58"
        auth_token = "57b97050ef022563dc9a08f105900e5a"
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=text,
            from_='+16143680119',
            to= phone_number
        )



    def get_cat_facts(self):
        return requests.get(url="https://catfact.ninja/fact").json()["fact"]


root = tk.Tk(className="Cat Facts")
root.geometry("600x400")
app = gui_stuff(master=root)
app.mainloop()




