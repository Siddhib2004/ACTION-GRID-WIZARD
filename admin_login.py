import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import mysql.connector  # direct DB connection

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

LOGO_PATH = "/mnt/data/89318221-80c2-42de-8835-a636834e4cc1.png"

# DB config (change user/password/db as per your XAMPP setup)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # default XAMPP MySQL password
    'database': 'geccs_activity_system'
}

class AdminLogin(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GECCS Activity System - Admin Login")
        self.geometry("1400*600")
        self.minsize(1400, 600)
        self.configure(fg_color="#F7F7F7")
        self._build_ui()
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=20)
        logo = self._load_logo()
        if logo:
            lbl_logo = ctk.CTkLabel(header, image=logo, text="")
            lbl_logo.image = logo
            lbl_logo.pack(side="left", padx=20)
        ctk.CTkLabel(header, text="Admin Login", font=("Segoe UI", 28, "bold"),
                     text_color="#003333").pack(side="left", padx=10)

        # Main card
        card = ctk.CTkFrame(self, width=700, height=400, corner_radius=20)
        card.pack(pady=30)
        card.pack_propagate(False)

        form = ctk.CTkFrame(card, fg_color="transparent")
        form.place(relx=0.5, rely=0.5, anchor="center")

        LABEL_FONT = ("Segoe UI", 16)
        ENTRY_WIDTH = 350
        PAD_Y = 12

        # Fields
        ctk.CTkLabel(form, text="User ID", font=LABEL_FONT).grid(row=0, column=0, sticky="w", pady=PAD_Y)
        self.user_id = ctk.CTkEntry(form, width=ENTRY_WIDTH, placeholder_text="Enter User ID")
        self.user_id.grid(row=0, column=1, pady=PAD_Y)

        ctk.CTkLabel(form, text="Password", font=LABEL_FONT).grid(row=1, column=0, sticky="w", pady=PAD_Y)
        self.password = ctk.CTkEntry(form, width=ENTRY_WIDTH, show="*", placeholder_text="Enter Password")
        self.password.grid(row=1, column=1, pady=PAD_Y)

        ctk.CTkLabel(form, text="Department  ", font=LABEL_FONT).grid(row=2, column=0, sticky="w", pady=PAD_Y)
        self.department = ctk.CTkOptionMenu(form, values=["CSE", "IT", "ENTC", "EEE", "MECH", "CIVIL", "AUTO"], width=ENTRY_WIDTH)
        self.department.set("ENTC")
        self.department.grid(row=2, column=1, pady=PAD_Y)

        # Buttons
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.place(relx=0.5, rely=0.85, anchor="center")

        self.login_btn = ctk.CTkButton(btn_frame, text="Login", width=180, height=45,
                                       fg_color="#007acc", command=self.authenticate)
        self.login_btn.pack(side="left", padx=10)

        self.back_btn = ctk.CTkButton(btn_frame, text="Back", width=180, height=45,
                                      fg_color="#6c757d", command=self.back_to_main)
        self.back_btn.pack(side="left", padx=10)

    def _load_logo(self):
        if os.path.exists(LOGO_PATH):
            img = Image.open(LOGO_PATH).convert("RGBA")
            img = img.resize((100, 100), Image.LANCZOS)
            return ctk.CTkImage(light_image=ImageTk.PhotoImage(img), size=(100, 100))
        return None

    def get_connection(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"DB connection failed: {e}")
            return None

    def authenticate(self):
        user_id = self.user_id.get().strip()
        password = self.password.get().strip()
        department = self.department.get()

        if not user_id or not password:
            messagebox.showwarning("Missing fields", "Please enter User ID and Password.")
            return

        conn = self.get_connection()
        if not conn:
            return

        try:
            cur = conn.cursor()
            sql = """SELECT username FROM users 
                     WHERE user_id=%s AND password=%s 
                     AND department=%s AND role='admin'"""
            cur.execute(sql, (user_id, password, department))
            res = cur.fetchone()
            if res:
                messagebox.showinfo("Success", f"Welcome {res[0]}!")
                self.destroy()
                from admin_dashboard import AdminDashboard  # ensure this is your file name
                dashboard = AdminDashboard()
                dashboard.mainloop()

            else:
                messagebox.showerror("Invalid", "Incorrect login credentials.")
        except Exception as e:
            messagebox.showerror("Database Error", f"{e}")
        finally:
            if conn.is_connected():
                conn.close()

    def back_to_main(self):
        self.destroy()
        from mainlog import MainMenu
        app = MainMenu()
        app.mainloop()


if __name__ == "__main__":
    app = AdminLogin()
    app.mainloop()
