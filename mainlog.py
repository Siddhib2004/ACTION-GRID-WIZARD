import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import mysql.connector

# ---------- Config ----------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
DB = dict(host="localhost", user="root", password="", database="geccs")


# ---------- Helpers ----------
def db_connect():
    try:
        return mysql.connector.connect(**DB)
    except mysql.connector.Error as e:
        messagebox.showerror("DB Error", str(e))
        return None


# ---------- Main Menu App ----------
class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GECCS - Main Menu")
        self.geometry("1400*600")
        self.minsize(1400, 600)
        self.resizable(True , True)
        self.eval('tk::PlaceWindow . center')

        self._build_ui()

    def _build_ui(self):
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=50, pady=50)

        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(pady=(40, 20))

        ctk.CTkLabel(header_frame, text="GECCS",
                     font=("Segoe UI", 32, "bold"),
                     text_color="#0B3D3E").pack(pady=10)

        ctk.CTkLabel(header_frame, text="Government College Of Engineering Chhatrapati Sambhajinagar",
                     font=("Segoe UI", 20),
                     text_color="#5a6b76").pack(pady=5)

        ctk.CTkLabel(header_frame, text="(Aurangabad)",
                     font=("Segoe UI", 16),
                     text_color="#5a6b76").pack(pady=5)

        # Separator
        sep = ttk.Separator(main_frame, orient="horizontal")
        sep.pack(fill="x", padx=40, pady=20)

        # Buttons Frame
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(pady=40, fill="both", expand=True)

        # Admin Login Button
        admin_btn = ctk.CTkButton(buttons_frame,
                                  text="ADMIN LOGIN",
                                  width=300,
                                  height=60,
                                  fg_color="#0A66C2",
                                  hover_color="#085aa6",
                                  font=("Segoe UI", 20, "bold"),
                                  command=self.admin_login)
        admin_btn.pack(pady=15)

        # Faculty Login Button
        faculty_btn = ctk.CTkButton(buttons_frame,
                                    text="FACULTY LOGIN",
                                    width=300,
                                    height=60,
                                    fg_color="#1070D6",
                                    hover_color="#0b5fb0",
                                    font=("Segoe UI", 20, "bold"),
                                    command=self.faculty_login)
        faculty_btn.pack(pady=15)

        # User Registration Button
        register_btn = ctk.CTkButton(buttons_frame,
                                     text="USER REGISTRATION",
                                     width=300,
                                     height=60,
                                     fg_color="#28a745",
                                     hover_color="#218838",
                                     font=("Segoe UI", 20, "bold"),
                                     command=self.user_registration)
        register_btn.pack(pady=15)

        # Back to Login Button
        back_btn = ctk.CTkButton(buttons_frame,
                                 text="BACK TO LOGIN",
                                 width=300,
                                 height=60,
                                 fg_color="#6c757d",
                                 hover_color="#5a6268",
                                 font=("Segoe UI", 20, "bold"),
                                 command=self.back_to_login)
        back_btn.pack(pady=15)

    def admin_login(self):
        """Open Admin Login Window"""
        self.destroy()
        from admin_login import AdminLogin
        app = AdminLogin()
        app.mainloop()

    def faculty_login(self):
        """Open Faculty Login Window"""
        self.destroy()
        from faculty_login import FacultyLogin
        app = FacultyLogin()
        app.mainloop()

    def user_registration(self):
        """Open User Registration Window"""
        self.destroy()
        from registration import Registration
        app = Registration()
        app.mainloop()

    def back_to_login(self):
        """Go back to main login screen"""
        self.destroy()
        from login import Login
        app = Login()
        app.mainloop()


# ---------- Run ----------
if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()