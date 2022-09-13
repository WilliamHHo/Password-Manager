from tkinter import *
from tkinter import messagebox
import pyperclip
from random import randint, choice, shuffle
import json


# ---------------------------- SEARCH ------------------------------- #
def search():
    web = web_input.get()
    try:
        with open('data.json') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title='Error', message="No data exists currently")
    else:
        if web in data:
            email = data[web]['email']
            password = encryption(data[web]['password'], shift, "decode")
            messagebox.showinfo(title=web, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"{web} doesn't have an existing password")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
           'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def gen_password():
    gen_pass = [choice(letters) for _ in range(randint(8, 10))] + [choice(symbols) for _ in range(randint(2, 4))] + [
        choice(numbers) for _ in range(randint(2, 4))]
    shuffle(gen_pass)
    new_password = "".join(gen_pass)
    pass_input.insert(0, new_password)
    pyperclip.copy(new_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    web = web_input.get()
    email = email_input.get()
    password = encryption(pass_input.get(), shift, "encode")
    new_data = {web: {
        'email': email,
        'password': password,
    }
    }
    if len(web) < 1 or len(password) < 1:
        messagebox.showinfo(title='Error', message='Not all fields are filled in')
    else:
        try:
            with open('data.json', 'r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open('data.json', 'w') as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            web_input.delete(0, END)
            pass_input.delete(0, END)


# ---------------------------- ENCRYPTION MODEL ------------------------------- #
shift = 2


def encryption(start_text, shift_amount, cipher_direction):
    end_text = ""
    if cipher_direction == "decode":
        shift_amount *= -1
    for char in start_text:
        if char in letters:
            position = letters.index(char)
            new_position = abs((position + shift_amount) % 52)
            end_text += letters[new_position]
        elif char in numbers:
            position = numbers.index(char)
            new_position = abs((position + shift_amount) % 10)
            end_text += numbers[new_position]
        elif char in symbols:
            position = symbols.index(char)
            new_position = abs((position + shift_amount) % 9)
            end_text += symbols[new_position]
        else:
            end_text += char

    return end_text


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title('Password Manager')
window.config(padx=20, pady=20)
canvas = Canvas(width=200, height=200)
logo = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

web_label = Label(text='Website: ')
web_label.grid(column=0, row=1)
email_label = Label(text='Email/Username:')
email_label.grid(column=0, row=2)
email_label = Label(text='Password:')
email_label.grid(column=0, row=3)

web_input = Entry(width=32)
web_input.grid(column=1, row=1, sticky="W")
web_input.focus()
email_input = Entry(width=52)
email_input.grid(column=1, row=2, columnspan=2, sticky="W")
pass_input = Entry(width=32)
pass_input.grid(column=1, row=3, sticky="W")

search_button = Button(text="Search", width=15, command=search)
search_button.grid(column=2, row=1, columnspan=1)
gen_button = Button(text="Generate Password", width=15, command=gen_password)
gen_button.grid(column=2, row=3, columnspan=1)
add_button = Button(text="Add", width=44, command=save)
add_button.grid(column=1, row=4, columnspan=2, sticky="W")
window.mainloop()
