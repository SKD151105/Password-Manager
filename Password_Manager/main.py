from tkinter import *
from tkinter import messagebox  # This is not a class and hence has to be imported separately
from random import randint, shuffle, choice
import pyperclip
import json


class PasswordManager:

    def __init__(self, master):
        self.email_label = None
        self.password_label = None
        self.add_button = None
        self.website_label = None
        self.canvas = None
        self.generate_password_button = None
        self.search_button = None
        self.master = master
        self.master.title("Password Manager")
        self.master.config(padx=50, pady=50)

        self.user_verified = False
        self.error_found = False
        self.error_label = None
        self.website_entry = None
        self.email_entry = None
        self.password_entry = None
        self.logo_img = None

        self.user = Label(text="Enter key:")
        self.user.grid(row=0, column=0)
        self.key = Entry(show="*")
        self.key.focus()
        self.key.grid(row=0, column=1)
        self.enter = Button(text="Enter", command=self.check)
        self.enter.grid(row=0, column=2)

    def generate_password(self):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                   'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                   'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                   'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        nr_letters = randint(8, 10)
        nr_symbols = randint(2, 4)
        nr_numbers = randint(2, 4)

        password_letters = [choice(letters) for _ in range(nr_letters)]
        password_symbols = [choice(symbols) for _ in range(nr_symbols)]
        password_numbers = [choice(numbers) for _ in range(nr_numbers)]

        password_list = password_numbers + password_symbols + password_letters
        shuffle(password_list)

        password = "".join(password_list)
        self.password_entry.insert(0, password)
        pyperclip.copy(password)

    def save(self):
        website = self.website_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        new_data = {
            website: {
                "email": email,
                "password": password
            }
        }

        if len(website) == 0 or len(password) == 0 or len(email) == 0:
            messagebox.showinfo(title="Oops", message="Please do not leave any field empty!")
        else:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)  # Reading old data

            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            else:
                data.update(new_data)  # Updating old data with new data
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)  # Saving updated data

            finally:
                self.website_entry.delete(0, END)
                self.password_entry.delete(0, END)

    def find_password(self):
        website = self.website_entry.get().capitalize()
        if len(website) == 0:
            messagebox.showinfo(title="Oops", message="Enter the name of the site!")
        else:
            try:
                with open("data.json") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                messagebox.showinfo(title="Oops", message="Data Not Found.")
            else:
                if website in data:
                    email = data[website]["email"]
                    password = data[website]["password"]
                    messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
                    pyperclip.copy(password)
                else:
                    messagebox.showinfo(title="Error", message=f"No details for {website} exists.")

    def create_ui(self):
        self.canvas = Canvas(height=200, width=200)
        self.logo_img = PhotoImage(file="logo.png")
        self.canvas.create_image(116, 100, image=self.logo_img)
        self.canvas.grid(row=0, column=1)

        # Labels
        self.website_label = Label(text="Website:")
        self.website_label.grid(row=1, column=0)
        self.email_label = Label(text="Email/Username:")
        self.email_label.grid(row=2, column=0)
        self.password_label = Label(text="Password:")
        self.password_label.grid(row=3, column=0)

        # Entries
        self.website_entry = Entry(width=23)
        self.website_entry.grid(row=1, column=1, columnspan=1)
        self.website_entry.focus()
        self.email_entry = Entry(width=40)
        self.email_entry.grid(row=2, column=1, columnspan=2)
        self.email_entry.insert(0, "5318752shubham.class10@gmail.com")
        self.password_entry = Entry(width=23)
        self.password_entry.grid(row=3, column=1)

        # Buttons
        self.search_button = Button(text="Search", width=16, command=self.find_password)
        self.search_button.grid(row=1, column=2)
        self.generate_password_button = Button(text="Generate Password", command=self.generate_password)
        self.generate_password_button.grid(row=3, column=2)
        self.add_button = Button(text="Add", width=42, command=self.save)
        self.add_button.grid(row=4, column=1, columnspan=2)

    def check(self):
        if self.key.get() == "skd1545":
            self.user.destroy()
            self.key.destroy()
            self.enter.destroy()
            if self.error_found:
                self.error_label.destroy()
            self.user_verified = True
            self.create_ui()
        else:
            self.error_found = True
            self.key.delete(0, END)
            self.error_label = Label(text="Incorrect key. Please try again.")
            self.error_label.grid(row=1, column=0, columnspan=3)


if __name__ == "__main__":
    root = Tk()
    app = PasswordManager(root)
    root.mainloop()
