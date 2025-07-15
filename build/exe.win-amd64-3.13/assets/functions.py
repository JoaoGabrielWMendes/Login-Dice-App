import customtkinter as ctk
import sqlite3
con = sqlite3.connect("users.db")
cur = con.cursor()
def entry_fields(label_text,entry_placeholder):
    label=ctk.CTkLabel(entry_placeholder,text=label_text)
    label.pack()
    entry=ctk.CTkEntry(entry_placeholder, show="*" if label_text=="Password" else "")
    entry.pack()
    return entry
def clear(app):
    for widget in app.winfo_children():
        widget.destroy()
