# 🎲 Login Dice App

A graphical application built with **Python** and **CustomTkinter** that allows users to create accounts, log in, roll a dice, and save each result to an SQLite database.

## ✨ Features

- 📋 **User Registration** with input validation (no empty fields or duplicate usernames).
- 🔐 **User Login** with credential verification.
- 🎯 **Dice Rolling** (1 to 20) with automatic result logging.
- 🕓 **Roll History** per user, showing the date and time.
- 💾 **SQLite Database** with two tables:
  - `users`: Stores usernames and passwords.
  - `rolls`: Stores dice roll results linked to user accounts.

## 🛠️ Tech Stack

- Python 3.x
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Pillow (PIL)
- SQLite3 (built-in with Python)