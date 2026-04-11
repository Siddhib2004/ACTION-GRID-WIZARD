import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# keep your existing Database helper
from database import Database

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


LOGO_URL = "sandbox:/mnt/data/89318221-80c2-42de-8835-a636834e4cc1.png"
LOCAL_LOGO_PATH = "/mnt/data/89318221-80c2-42de-8835-a636834e4cc1.png"


class Registration(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GECCS Activity System - Registration")
        self.geometry("1000x600")
        self.minsize(1400, 600)
        self.resizable(True , True)
        self.configure(fg_color="#F7F7F7")
        self._build_ui()

    def _build_ui(self):
        # top area with optional logo + title
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=(20, 0))

        # Try to load logo if available (fall back to text)
        logo_frame = ctk.CTkFrame(top, fg_color="transparent")
        logo_frame.pack(side="left", padx=30)
        logo_img = self._load_logo()
        if logo_img:
            lbl_logo = ctk.CTkLabel(logo_frame, image=logo_img, text="")
            lbl_logo.image = logo_img  # keep reference
            lbl_logo.pack()
        else:
            ctk.CTkLabel(logo_frame, text="User Registration", font=("Segoe UI", 28, "bold"),
                         text_color="#003333").pack()

        #ctk.CTkLabel(top, text="User Registration",
                     #font=("Segoe UI", 28, "bold"),
                     #text_color="#003333").pack(side="left", padx=20, pady=(10, 0))

        # Main card
        card = ctk.CTkFrame(self, width=880, height=520, corner_radius=20)
        card.pack(pady=30)
        card.pack_propagate(False)

        # layout inside card: left labels, right inputs
        form = ctk.CTkFrame(card, fg_color="transparent")
        form.place(relx=0.5, rely=0.5, anchor="center")

        LABEL_FONT = ("Segoe UI", 16)
        ENTRY_WIDTH = 360
        ENTRY_HEIGHT = 38
        PAD_Y = 8

        # Username
        ctk.CTkLabel(form, text="Username", font=LABEL_FONT).grid(row=0, column=0, sticky="w", padx=12, pady=(10, PAD_Y))
        self.username = ctk.CTkEntry(form, width=ENTRY_WIDTH, height=ENTRY_HEIGHT, placeholder_text="Enter full name")
        self.username.grid(row=0, column=1, padx=12, pady=(10, PAD_Y))

        # Department (OptionMenu)
        ctk.CTkLabel(form, text="Department", font=LABEL_FONT).grid(row=1, column=0, sticky="w", padx=12, pady=PAD_Y)
        self.department = ctk.CTkOptionMenu(form, values=["CSE", "IT", "ENTC", "EEE", "MECH", "CIVIL", "AUTO"], width=ENTRY_WIDTH)
        self.department.set("ENTC")
        self.department.grid(row=1, column=1, padx=12, pady=PAD_Y)

        # Status
        ctk.CTkLabel(form, text="Status", font=LABEL_FONT).grid(row=2, column=0, sticky="w", padx=12, pady=PAD_Y)
        self.status = ctk.CTkOptionMenu(form, values=["Regular", "Visitor"], width=ENTRY_WIDTH)
        self.status.set("Regular")
        self.status.grid(row=2, column=1, padx=12, pady=PAD_Y)

        # User ID
        ctk.CTkLabel(form, text="User ID", font=LABEL_FONT).grid(row=3, column=0, sticky="w", padx=12, pady=PAD_Y)
        self.user_id = ctk.CTkEntry(form, width=ENTRY_WIDTH, height=ENTRY_HEIGHT, placeholder_text="Unique user identifier")
        self.user_id.grid(row=3, column=1, padx=12, pady=PAD_Y)

        # Password
        ctk.CTkLabel(form, text="Password", font=LABEL_FONT).grid(row=4, column=0, sticky="w", padx=12, pady=PAD_Y)
        self.password = ctk.CTkEntry(form, width=ENTRY_WIDTH, height=ENTRY_HEIGHT, show="*", placeholder_text="Choose a password")
        self.password.grid(row=4, column=1, padx=12, pady=PAD_Y)

        # Role
        ctk.CTkLabel(form, text="Role", font=LABEL_FONT).grid(row=5, column=0, sticky="w", padx=12, pady=PAD_Y)
        self.role = ctk.CTkOptionMenu(form, values=["Faculty", "Admin"], width=ENTRY_WIDTH)
        self.role.set("Faculty")
        self.role.grid(row=5, column=1, padx=12, pady=PAD_Y)

        # Buttons
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.place(relx=0.5, rely=0.92, anchor="center")

        self.register_btn = ctk.CTkButton(btn_frame, text="Register", width=180, height=45, corner_radius=10,
                                          fg_color="#007acc", hover=True, command=self.register_user)
        self.register_btn.pack(side="left", padx=10)

        self.back_btn = ctk.CTkButton(btn_frame, text="Back to Login", width=220, height=45, corner_radius=10,
                                      fg_color="#6c757d", hover=True, command=self.back_to_login)
        self.back_btn.pack(side="left", padx=10)

    def _load_logo(self):
        # try both the sandbox url and local path; return a CTk-compatible image (PIL->CTk)
        for p in (LOCAL_LOGO_PATH, LOGO_URL):
            try:
                if not os.path.exists(p):
                    # sometimes LOGO_URL is in sandbox: form; try removing prefix
                    maybe = p.replace("sandbox:", "")
                else:
                    maybe = p
                if os.path.exists(maybe):
                    img = Image.open(maybe).convert("RGBA")
                    img = img.resize((100, 100), Image.LANCZOS)
                    return ctk.CTkImage(light_image=ImageTk.PhotoImage(img), size=(100, 100))
            except Exception:
                continue
        return None

    def get_connection(self):
        try:
            return Database.get_connection()
        except Exception as e:
            messagebox.showerror("Database Error", f"DB connection failed: {e}")
            return None

    def register_user(self):
        username = self.username.get().strip()
        department = self.department.get()
        status = self.status.get()
        user_id = self.user_id.get().strip()
        password = self.password.get().strip()
        role = self.role.get().lower()

        # validation (same as your Java logic)
        if not username or not user_id or not password:
            messagebox.showwarning("Missing fields", "Please fill Username, User ID and Password.")
            return

        conn = self.get_connection()
        if conn is None:
            return

        try:
            cur = conn.cursor()
            # duplicate check
            check_sql = "SELECT user_id FROM users WHERE user_id = %s"
            cur.execute(check_sql, (user_id,))
            if cur.fetchone():
                messagebox.showerror("Duplicate", "User ID already exists!")
                return

            insert_sql = """INSERT INTO users 
                            (username, department, status, user_id, password, role) 
                            VALUES (%s, %s, %s, %s, %s, %s)"""
            cur.execute(insert_sql, (username, department, status, user_id, password, role))
            conn.commit()

            if cur.rowcount > 0:
                messagebox.showinfo("Success", "Registration Successful!")
                # close this window and optionally open login
                self.destroy()
                messagebox.showinfo("Redirect", "Redirecting to login (implement login opener).")
            else:
                messagebox.showerror("Failed", "Registration failed. Try again.")
        except Exception as ex:
            messagebox.showerror("Database Error", f"Error: {ex}")
        finally:
            try:
                if conn and getattr(conn, "is_connected", lambda: True)():
                    conn.close()
            except Exception:
                pass

    def back_to_login(self):
        # close and signal login to open (you can implement a callback instead)

        self.destroy()
        from login import Login
        app = Login()
        app.mainloop()
if __name__ == "__main__":
    app = Registration()
    app.mainloop()
