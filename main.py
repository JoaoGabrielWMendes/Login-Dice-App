import customtkinter as ctk
import sqlite3
import random
import pytz
import os 
import shutil
from datetime import datetime
from PIL import Image, ImageTk, ImageSequence
from customtkinter import CTkImage
from assets.functions import entry_fields, clear
from tkinter import filedialog
app = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
success_img_PIL=Image.open("assets/success.png")
success_img = CTkImage(dark_image=success_img_PIL, size=(200, 200))
dice_img_PIL=Image.open("assets/dice_twenty_sides.png")
dice_img=CTkImage(dark_image=dice_img_PIL, size=(100,100))
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
current_password= None
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
    create_account_button=ctk.CTkButton(app,text="Create Account",fg_color="transparent",command=lambda: [clear(app), create_account()])
    create_account_button.pack(pady=(2,0))
    label_error = ctk.CTkLabel(app, text="")
    label_error.pack()
    def check_login():
        global current_user, current_password
        cursor.execute("SELECT 1 FROM users WHERE username=? AND password=?", (login_username_entry.get(), login_password_entry.get()))
        if cursor.fetchone():
            current_user=login_username_entry.get()
            current_password=login_password_entry.get()
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
    button_back_login=ctk.CTkButton(app, text="Back",fg_color="transparent", font=("", 14), command=lambda: [clear(app), show_login_screen()])
    button_back_login.pack(pady=10)
def create_account():
    create_account_label_title=ctk.CTkLabel(app,text="Create Account",font=("", 25))
    create_account_label_title.pack(pady=10)
    create_account_username_entry=entry_fields("Username", app)
    create_account_password_entry=entry_fields(" Password ", app)
    create_account_button_submit=ctk.CTkButton(app,text="Create Account",command=lambda: [insert_user()])
    create_account_button_submit.pack(pady=(15,5))
    button_back_login=ctk.CTkButton(app,text="Back",fg_color="transparent",command=show_login_screen)
    button_back_login.pack(pady=(2,0))
    error_label = ctk.CTkLabel(app, text="", font=("", 12))
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
    roll_label_title = ctk.CTkLabel(app, text="Roll the Dice", font=("Poppins", 25, "bold"))
    roll_label_title.pack(pady=10)
    value_entry = entry_fields("How many sides will the dice have?", app)
    warning_label = ctk.CTkLabel(app, text="")
    gif = Image.open("assets/dice_twenty_sides_gif.gif")
    frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA").resize((100, 100))) for frame in ImageSequence.Iterator(gif)]
    gif_label = ctk.CTkLabel(app, text="", image=frames[0])
    gif_label.pack(pady=20)
    def animate(index=0):
        global animation_job
        gif_label.configure(image=frames[index])
        animation_job=app.after(100, lambda: animate((index+1)%len(frames)))
    def roll_dice():
        global current_user
        try:
            sides = int(value_entry.get())
            roll_result = random.randint(1, sides)
        except ValueError:
            warning_label.configure(text="Invalid input. Please enter a positive number.", font=("Roboto", 12, "italic"))
            return
        roll_button.configure(state="disabled", text="Rolling...")
        warning_label.configure(text="")
        br_tz=pytz.timezone("America/Sao_Paulo")
        now_br=datetime.now(br_tz).strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO rolls (user_id, roll_result, timestamp) VALUES ((SELECT id FROM users WHERE username=?), ?, ?)", (current_user, roll_result, now_br))
        gif_label.configure(text="")
        animate()
        def show_result_label2():
            if animation_job:
                app.after_cancel(animation_job)
            gif_label.configure(text=roll_result, image=dice_img, font=("", 23, "bold"),text_color="black")
            roll_button.configure(state="normal", text="Roll the dice")
        app.after(3000, show_result_label2)

    roll_button = ctk.CTkButton(app, text="Roll the dice", command=lambda:[roll_dice()])
    roll_button.pack(pady=10)
    user_configuration_button=ctk.CTkButton(app, text="User Configurations", command=lambda: [clear(app), user_configuration()])
    user_configuration_button.pack(pady=5)
    back_button = ctk.CTkButton(app, text="Back to Login", fg_color="transparent", command=show_login_screen)
    back_button.pack(pady=(5, 20))
    warning_label.pack(pady=10)
def user_configuration():
    global current_user, confirmation_screen_open
    user_configuration_title=ctk.CTkLabel(app, text=f"Hello, {current_user}!", font=("Poppins",25, "bold"))
    user_configuration_title.pack(pady=10)
    history_rolls_button=ctk.CTkButton(app, text="View Roll History", command=lambda: [clear(app), display_roll_history()])
    history_rolls_button.pack(pady=5)
    def confirmation_screen():
        global confirm_window,confirmation_screen_open
        confirmation_screen_open=True
        confirm_window=ctk.CTkToplevel(app)
        confirm_window.title("Confirmation")
        confirm_window.geometry("300x150")
        confirm_window.grab_set()
        confirm_window.focus_set()
        label_title=ctk.CTkLabel(confirm_window, text="Are you sure?")
        label_title.pack(pady=20)
        def confirm():
            global current_user, current_password
            cursor.execute("DELETE FROM users WHERE id=(SELECT id FROM users WHERE username=?)",(current_user,))
            conn.commit()
            current_user = None
            current_password = None
            confirm_window.destroy()
            return show_login_screen()
        def cancel():
            global confirmation_screen_open
            confirm_window.destroy()
        confirm_button=ctk.CTkButton(confirm_window, text="Yes", command=confirm)
        confirm_button.pack(side="left", padx=10, pady=10)
        cancel_button=ctk.CTkButton(confirm_window, text="No", fg_color="transparent", command=cancel)
        cancel_button.pack(side="right", padx=10, pady=10)
    theme_button=ctk.CTkButton(app, text="Theme", command=change_theme)
    theme_button.pack(pady=10)
    delete_user_button=ctk.CTkButton(app, text="Delete user", command=confirmation_screen)
    delete_user_button.pack(pady=5)
    back_button = ctk.CTkButton(app, text="Back to Roll dice", fg_color="transparent", command=display_roll_dice)
    back_button.pack(pady=(5, 20))
def change_theme():
    clear(app)
    scrollable_frame = ctk.CTkScrollableFrame(app, width=380, height=380, fg_color="transparent" )
    scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
    roll_label_title = ctk.CTkLabel(scrollable_frame, text="Change Theme", font=("Poppins", 25, "bold"))
    roll_label_title.pack(pady=10)
    themes = {
        "dark blue": "dark-blue",
    }
    theme_dir=os.path.join("assets", "themes")
    if os.path.exists(theme_dir):
        for file in os.listdir(theme_dir):
            if file.endswith(".json"):
                themes[file.replace(".json","")]=os.path.join(theme_dir,file)
    for theme_name, theme_file in themes.items():
            theme_button = ctk.CTkButton(scrollable_frame, text=theme_name, command=lambda tf= theme_file: [apply_theme(tf), change_theme()])
            theme_button.pack(pady=5)
    def apply_theme(theme_file):
        ctk.set_default_color_theme(theme_file)
    def load_custom_theme():
        file_path=filedialog.askopenfilename(title="Select a theme file",filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                os.makedirs(theme_dir, exist_ok=True)
                file_name=os.path.basename(file_path)
                dest_path=os.path.join(theme_dir, file_name)
                shutil.copy(file_path, dest_path)
                change_theme()
            except Exception as e:
                error_label=ctk.CTkLabel(scrollable_frame, text=f"Error loading custom theme: {e}")
                error_label.pack(pady=5)
    def explanation():
        change_theme_window = ctk.CTkToplevel(app)
        change_theme_window.title("Import Theme")
        change_theme_window.geometry("400x300")
        change_theme_window.grab_set()
        change_theme_window.focus_set()
        label_title = ctk.CTkLabel(change_theme_window,text="How to import a theme?",font=("Poppins",25, "bold"))
        label_title.pack(pady=20)
        label_instructions = ctk.CTkLabel(change_theme_window,text="1. Download a theme JSON file.\n2. Click 'Load Custom Theme'.\n3. Select the downloaded file.\n4. The theme will be on 'Change Theme' list.\n5. Click the theme to apply it.")
        label_instructions.pack(pady=10)
        change_theme_button = ctk.CTkButton(change_theme_window, text="Load custom theme", command=lambda: [load_custom_theme(), change_theme_window.destroy()])
        change_theme_button.place(relx=0.1, rely=0.65)
        button_close = ctk.CTkButton(change_theme_window, text="Close", fg_color="transparent", command=change_theme_window.destroy)
        button_close.place(relx=0.55, rely=0.65)
    load_custom_theme_button = ctk.CTkButton(scrollable_frame, text="Load your theme", command=explanation)
    load_custom_theme_button.pack(pady=5)
    back_button = ctk.CTkButton(scrollable_frame, text="Back to User configuration", fg_color="transparent", command=lambda: [clear(app), user_configuration()])
    back_button.pack(pady=(5, 20))
def display_roll_history():
    clear(app)
    scrollable_frame = ctk.CTkScrollableFrame(app, width=380, height=380, fg_color="transparent")
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
    delete_history=("DELETE FROM rolls WHERE user_id=(SELECT id FROM users WHERE username=?)", (current_user,))
    clear_button = ctk.CTkButton(scrollable_frame, text="Clear History",command=lambda: [cursor.execute(*delete_history), conn.commit(), clear(app), display_roll_history()])
    clear_button.pack(pady=5)
    back_button = ctk.CTkButton(scrollable_frame, text="Back to User configuration", fg_color="transparent", command=lambda: [clear(app), user_configuration()])
    back_button.pack(pady=(5, 20))
def delete_user():
    global current_user, current_password
    cursor.execute("DELETE FROM users WHERE id=(SELECT id FROM users WHERE username=?)",(current_user,))
    conn.commit()
    current_user = None
    current_password = None
    return show_login_screen()
def on_close():
    conn.close()
    app.destroy()
app.protocol("WM_DELETE_WINDOW", on_close)
app.mainloop()