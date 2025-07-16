import customtkinter as ctk
import sqlite3
import random 
from PIL import Image
from customtkinter import CTkImage
from assets.functions import entry_fields, clear
app = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
success_img_PIL=Image.open("assets/success.png")
success_img = CTkImage(dark_image=success_img_PIL, size=(200, 200))
app.title("Login test")
app.geometry("500x500")
app.resizable(False, False)
conn=sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE CHECK (username <> ''), password TEXT NOT NULL CHECK (password <> ''))")
cursor.execute("CREATE TABLE IF NOT EXISTS rolls (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, roll_result INTEGER NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (user_id) REFERENCES users(id))")
conn.commit()
cursor.execute
current_user = None
def show_login_screen():
    clear(app)
    login()
def login():
    global login_username_entry,current_user
    login_label_title = ctk.CTkLabel(app, text="Login",font=("", 25))
    login_label_title.pack(pady=10)
    login_username_entry=entry_fields("Username", app)
    login_password_entry=entry_fields("Password", app)
    login_button_submit = ctk.CTkButton(app, text="Login", command=lambda: [check_login()])
    login_button_submit.pack(pady=(15,5))
    create_account_button=ctk.CTkButton(app,text="Create Account",fg_color="transparent",text_color="#1f538d",command=lambda: [clear(app), create_account()])
    create_account_button.pack(pady=(2,0))
    label_error = ctk.CTkLabel(app, text="")
    label_error.pack()
    def check_login():
        global current_user
        cursor.execute("SELECT 1 FROM users WHERE username=? AND password=?", (login_username_entry.get(), login_password_entry.get()))
        if cursor.fetchone():
            current_user=login_username_entry.get()
            return login_success()
        else:
            label_error.configure(text="Invalid username or password.")
def login_success():
    clear(app)
    success_label_title = ctk.CTkLabel(app, text="Login Successful", font=("", 25))
    success_label_title.pack(pady=10)
    success_img_label=ctk.CTkLabel(app,image=success_img, text="")
    success_img_label.pack()
    button_continue=ctk.CTkButton(app, text="Continue", command=lambda: [clear(app), display_roll_dice()])
    button_continue.pack(pady=5)
    button_back_login=ctk.CTkButton(app, text="Back",fg_color="transparent",text_color="#1f538d", font=("", 14), command=lambda: [clear(app), show_login_screen()])
    button_back_login.pack(pady=10)
def create_account():
    create_account_label_title=ctk.CTkLabel(app,text="Create Account",font=("", 25))
    create_account_label_title.pack(pady=10)
    create_account_username_entry=entry_fields("Username", app)
    create_account_password_entry=entry_fields(" Password ", app)
    create_account_button_submit=ctk.CTkButton(app,text="Create Account",command=lambda: [insert_user()])
    create_account_button_submit.pack(pady=(15,5))
    button_back_login=ctk.CTkButton(app,text="Back",fg_color="transparent",text_color="#1f538d",command=show_login_screen)
    button_back_login.pack(pady=(2,0))
    error_label = ctk.CTkLabel(app, text="")
    error_label.pack()
    def insert_user():
        try:
            if not create_account_username_entry.get().strip() or not create_account_password_entry.get().strip():
                error_label.configure(text="Username or password cannot be empty.")
            else:
                cursor.execute("INSERT INTO users (username, password) VALUES(?,?)", (create_account_username_entry.get(), create_account_password_entry.get()))
                conn.commit()
                error_label.configure(text="")
                return show_login_screen()
        except sqlite3.IntegrityError as e:
            if 'CHECK constraint failed' in str(e):
                error_label.configure(text="Username or password cannot be empty.")
            else:
                error_label.configure(text="Username already exists.")
show_login_screen()
def display_roll_dice():
    clear(app)
    roll_label_title = ctk.CTkLabel(app, text="Roll the Dice", font=("", 25))
    roll_label_title.pack(pady=10)
    roll_result_label = ctk.CTkLabel(app, text="Ready to roll", font=("", 20))
    roll_result_label.pack(pady=10)
    def roll_dice():
        global current_user
        roll_result = random.randint(1, 20)
        cursor.execute("INSERT INTO rolls (user_id, roll_result) VALUES ((SELECT id FROM users WHERE username=?), ?)", (current_user, roll_result,))
        roll_result_label.configure(text=f"You rolled a {roll_result}")
    roll_button = ctk.CTkButton(app, text="Roll the dice", command=lambda:[roll_dice()])
    roll_button.pack(pady=10)
    history_rolls_button=ctk.CTkButton(app, text="View Roll History", command=lambda: [clear(app), display_roll_history()])
    history_rolls_button.pack(pady=5)
    back_button = ctk.CTkButton(app, text="Back to Login", fg_color="transparent", text_color="#1f538d", command=show_login_screen)
    back_button.pack(pady=(5, 20))
def display_roll_history():
    clear(app)
    scrollable_frame = ctk.CTkScrollableFrame(app, width=380, height=380)
    scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
    history_label_title = ctk.CTkLabel(scrollable_frame, text="Roll History", font=("", 25))
    history_label_title.pack(pady=10)
    cursor.execute("SELECT roll_result, timestamp FROM rolls WHERE user_id=(SELECT id FROM users WHERE username=?) ORDER BY timestamp DESC", (current_user,))
    rolls = cursor.fetchall()
    if rolls:
        for roll_result, timestamp in rolls:
            roll_label = ctk.CTkLabel(scrollable_frame, text=f"Rolled {roll_result} on {timestamp}", font=("", 16))
            roll_label.pack(pady=5)
    else:
        no_rolls_label = ctk.CTkLabel(scrollable_frame, text="No rolls found.", font=("", 16))
        no_rolls_label.pack(pady=5)
    back_button = ctk.CTkButton(scrollable_frame, text="Back to Roll Dice", fg_color="transparent", text_color="#1f538d", command=lambda: [clear(app), display_roll_dice()])
    back_button.pack(pady=(5, 20))
def on_close():
    conn.close()
    app.destroy()
app.protocol("WM_DELETE_WINDOW", on_close)
app.mainloop()