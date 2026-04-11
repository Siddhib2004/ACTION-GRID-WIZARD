import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class UserReg(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("User Registration")
        self.geometry("1000x600")
        self.minsize(1400, 600)
        ctk.CTkLabel(self, text="User Registration Page",
                     font=("Segoe UI", 24, "bold")).pack(pady=40)
        ctk.CTkButton(self, text="Close", command=self.destroy).pack(pady=20)


class Login(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title("GECCS Action Grid Wizard (An Activity Management System)")
        self.geometry("1000x600")
        self.resizable(True , True)
        self.configure(fg_color="#F5F5F5")  # light clean background

        # ----- MAIN TITLE -----
        ctk.CTkLabel(self,
                     text="GECCS",
                     font=("Georgia", 32, "bold"),
                     text_color="#003333",
                     fg_color="transparent").place(relx=0.5, rely=0.15, anchor="center")

        ctk.CTkLabel(self,
                     text="ACTION GRID WIZARD",
                     font=("Georgia", 52, "bold"),
                     text_color="#003333",
                     fg_color="transparent").place(relx=0.5, rely=0.25, anchor="center")

        # ----- LOGIN CARD -----
        card = ctk.CTkFrame(self,
                            width=520,
                            height=330,
                            corner_radius=25,
                            fg_color="#E8E8E8")
        card.place(relx=0.5, rely=0.58, anchor="center")

        # internal padding frame for clean alignment
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(pady=20)

        # ----- USER ID -----
        ctk.CTkLabel(inner,
                     text="User ID",
                     font=("Segoe UI", 18)).grid(row=0, column=0, padx=20, pady=15, sticky="w")

        self.txt_user = ctk.CTkEntry(inner,
                                     width=300,
                                     height=40,
                                     font=("Segoe UI", 16))
        self.txt_user.grid(row=0, column=1, padx=10, pady=15)

        # ----- PASSWORD -----
        ctk.CTkLabel(inner,
                     text="Password",
                     font=("Segoe UI", 18)).grid(row=1, column=0, padx=20, pady=15, sticky="w")

        self.txt_pass = ctk.CTkEntry(inner,
                                     width=300,
                                     height=40,
                                     font=("Segoe UI", 16),
                                     show="*")
        self.txt_pass.grid(row=1, column=1, padx=10, pady=15)

        # ----- LOGIN BUTTON -----
        ctk.CTkButton(inner,
                      text="Login",
                      width=160,
                      height=45,
                      font=("Segoe UI", 20, "bold"),
                      corner_radius=10,
                      command=self.login_action).grid(row=2, column=1, pady=25)

        # Exit button (top-right)
        #exit_b = ctk.CTkButton(self, text="X", fg_color="red",
                              # width=45, height=35, corner_radius=10,
                               #command=self.quit)
        #exit_b.place(relx=0.97, rely=0.04, anchor="ne")

    def login_action(self):
        user = self.txt_user.get().strip()
        password = self.txt_pass.get().strip()

        if not user or not password:
            messagebox.showwarning("Missing Info", "Please enter both fields.")
            return

        if user.lower() == "geccs" and password.lower() == "geccs":
            UserReg()
        else:
            messagebox.showerror("Invalid", "Invalid Credentials")

        self.destroy()
        from mainlog import MainMenu
        app = MainMenu()
        app.mainloop()


if __name__ == "__main__":
    app = Login()
    app.mainloop()
