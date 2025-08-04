# 🎲 Login Dice App

A graphical application built with **Python** and **CustomTkinter** that allows users to create accounts, log in, roll customizable dice, and save each result to an SQLite database.

## ✨ Features

- 📋 **User Registration & Login**
  - Input validation (no empty fields or duplicate usernames).
  - Credential verification at login.

- 🎲 **Custom Dice Rolling**
  - Choose the number of sides for the dice (not limited to d20).
  - Animated dice roll using GIFs.
  - Automatic result logging with timestamp.

- 🕓 **Roll History**
  - Each user has their own roll history.
  - Option to **clear history** directly from the app.

- 👤 **User Settings**
  - Personalized greeting.
  - View roll history.
  - **Delete account** (with confirmation window).
  - Access to theme customization.

- 🎨 **Theme System**
  - Built-in dark-blue theme.
  - Import and load **custom JSON themes**.
  - Theme manager with user-friendly interface.

- 💾 **SQLite Database**
  - `users`: Stores usernames and passwords.
  - `rolls`: Stores dice roll results linked to user accounts.

## 🛠️ Tech Stack

- Python 3.x
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Pillow (PIL)
- SQLite3 (built-in with Python)
- pytz (for accurate timestamps)

## 📂 Project Structure