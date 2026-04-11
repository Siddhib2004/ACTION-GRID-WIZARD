# main.py
import tkinter as tk
from tkinter import messagebox
from src.login import SimpleLoginForm

def main():
    try:
        # Start with login form
        app = SimpleLoginForm()
        app.run()
    except Exception as e:
        messagebox.showerror("Application Error", f"Failed to start application: {e}")

if __name__ == "__main__":
    main()