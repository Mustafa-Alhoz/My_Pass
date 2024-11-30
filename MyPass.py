from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from tkinter import messagebox
import pyperclip
import random
import json



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_numbers + password_symbols

    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty !!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \n\nEmail: {email} \nPassword: {password} \n\nIs it ok to save?")
        if is_ok:
            try:
                with open(relative_to_assets("data.json"), "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open(relative_to_assets("data.json"), "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)

                with open(relative_to_assets("data.json"), "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


def search():
    website = website_entry.get()
    try:
        with open(relative_to_assets("data.json"), "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists")


window = Tk()
window.title("MyPass")
window.geometry("500x500+500+100")
window.resizable(False, False)


canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file=relative_to_assets("logo.png"))
canvas.create_image(100, 100, image=logo_img)
canvas.place(x=145, y=10)


website_label = Label(text="Website:")
website_label.place(x=50, y=250)

email_label = Label(text="Email/Username:")
email_label.place(x=30, y=280)

password_label = Label(text="Password:")
password_label.place(x=47, y=310)


website_entry = Entry(width=36)
website_entry.place(x=130, y=250)
website_entry.focus()

email_entry = Entry(width=36)
email_entry.place(x=130, y=280)
email_entry.insert(0, "username@gmail.com")

password_entry = Entry(width=36)
password_entry.place(x=130, y=310)

generate_password_button = Button(text="Generate Password", command=generate_password, width= 20)
generate_password_button.place(x=360, y=307)

add_button = Button(text="Add", width=32, command=save)
add_button.place(x=137, y=340)

search_button = Button(text="Search", width=20, command=search)
search_button.place(x=360, y=249)


window.mainloop()
