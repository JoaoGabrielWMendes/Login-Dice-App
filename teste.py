import customtkinter as ctk
import sqlite3
from PIL import Image, ImageTk
window = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
image=Image.open("assets/success.png")
image_resize=image.resize((200,200))
window.iconbitmap("assets/icon.ico")
image_tk=ImageTk.PhotoImage(image_resize)
window.title("Login test")
window.geometry("500x500")
window.resizable(False, False)
con=sqlite3.connect("db.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS db (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE CHECK (username <> ''), password TEXT NOT NULL CHECK (password <> ''))")
con.commit()
cur.execute
def main():
    clear()
    login()
def login():
    label = ctk.CTkLabel(window, text="Login",font=("", 25))
    label.pack(pady=10)
    username= ctk.CTkLabel(window, text="Username")
    username.pack()
    username_entry=ctk.CTkEntry(window)
    username_entry.pack()
    password = ctk.CTkLabel(window,text="Password")
    password.pack()
    password_entry=ctk.CTkEntry(window, show="*")
    password_entry.pack()
    button = ctk.CTkButton(window, text="Login", command=lambda: [check_login()])
    button.pack(pady=(15,5))
    button_account=ctk.CTkButton(window,text="Create Account",fg_color="transparent",text_color="#1f538d",command=lambda: [clear(), create_account()])
    button_account.pack(pady=(2,0))
    label_error = ctk.CTkLabel(window, text="")
    label_error.pack()
    def check_login():
        cur.execute("SELECT 1 FROM db WHERE username=? AND password=?",(username_entry.get(),password_entry.get()))
        if cur.fetchone():
            return login_success()
        else:
            label_error.configure(text="Invalid username or password")
def login_success():
    clear()
    label = ctk.CTkLabel(window, text="Login Successful", font=("", 25))
    label.pack(pady=10)
    image_label=ctk.CTkLabel(window,image=image_tk, text="")
    image_label.pack()
    button_back=ctk.CTkButton(window, text="Back",fg_color="transparent",text_color="#1f538d", font=("", 14), command=lambda: [clear(), main()])
    button_back.pack(pady=10)
def create_account():
    label=ctk.CTkLabel(window,text="Create Account",font=("", 25))
    label.pack(pady=10)
    username=ctk.CTkLabel(window,text="Username")
    username.pack()
    username_entry=ctk.CTkEntry(window)
    username_entry.pack()
    password=ctk.CTkLabel(window,text="Password")
    password.pack()
    password_entry=ctk.CTkEntry(window)
    password_entry.pack()
    button=ctk.CTkButton(window,text="Create Account",command=lambda: [insert_db()])
    button.pack(pady=(15,5))
    button_back=ctk.CTkButton(window,text="Back",fg_color="transparent",text_color="#1f538d",command=main)
    button_back.pack(pady=(2,0))
    error_label = ctk.CTkLabel(window, text="")
    error_label.pack()
    def insert_db():
        try:
            if not username_entry.get().strip() or not password_entry.get().strip():
                error_label.configure(text="Username or password cannot be empty.")
            else:
                cur.execute("INSERT INTO db (username, password) VALUES(?,?)", (username_entry.get(),password_entry.get()))
                con.commit()
                print(f"Account {username_entry.get()} and {password_entry.get()} created")
                error_label.configure(text="")
                return main()
        except sqlite3.IntegrityError as e:
            if 'CHECK constraint failed' in str(e):
                error_label.configure(text="Username or password cannot be empty.")
            else:
                error_label.configure(text="Username already exists.")
def clear():
    for widget in window.winfo_children():
        widget.destroy()
main()
window.mainloop()