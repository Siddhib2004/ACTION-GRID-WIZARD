import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from datetime import datetime

# ---------- Config ----------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
DB = dict(host="localhost", user="root", password="", database="geccs")


class FacultyDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Faculty Dashboard")
        self.geometry("1400*600")
        self.minsize(1400, 600)
        self.eval('tk::PlaceWindow . center')

        # Variables
        self.activity_name_var = ctk.StringVar()
        self.club_name_var = ctk.StringVar()
        self.day_var = ctk.StringVar(value=str(datetime.now().day).zfill(2))
        self.month_var = ctk.StringVar(value=str(datetime.now().month).zfill(2))
        self.year_var = ctk.StringVar(value=str(datetime.now().year))
        self.start_hour_var = ctk.StringVar(value="09")
        self.start_minute_var = ctk.StringVar(value="00")
        self.start_ampm_var = ctk.StringVar(value="AM")
        self.end_hour_var = ctk.StringVar(value="10")
        self.end_minute_var = ctk.StringVar(value="00")
        self.end_ampm_var = ctk.StringVar(value="AM")

        self.build_ui()

    def build_ui(self):
        # Header
        header = ctk.CTkLabel(self, text="Faculty Dashboard", font=("Segoe UI", 28, "bold"))
        header.pack(pady=20)

        # Card frame
        card = ctk.CTkFrame(self, corner_radius=20, fg_color="white")
        card.pack(padx=24, pady=12, fill="both", expand=True)

        # Activity Name
        ctk.CTkLabel(card, text="Activity Name:", font=("Segoe UI", 20, "bold")).grid(row=0, column=0, sticky="w",
                                                                                      padx=20, pady=12)
        ctk.CTkEntry(card, textvariable=self.activity_name_var, font=("Segoe UI", 18)).grid(row=0, column=1, padx=20,
                                                                                            pady=12, sticky="ew")

        # Club Name
        ctk.CTkLabel(card, text="Club Name:", font=("Segoe UI", 20, "bold")).grid(row=1, column=0, sticky="w", padx=20,
                                                                                  pady=12)
        ctk.CTkEntry(card, textvariable=self.club_name_var, font=("Segoe UI", 18)).grid(row=1, column=1, padx=20,
                                                                                        pady=12, sticky="ew")

        # Date Pickers
        ctk.CTkLabel(card, text="Date:", font=("Segoe UI", 20, "bold")).grid(row=2, column=0, sticky="w", padx=20,
                                                                             pady=12)
        date_frame = ctk.CTkFrame(card, fg_color="transparent")
        date_frame.grid(row=2, column=1, sticky="w", padx=20, pady=12)
        ctk.CTkComboBox(date_frame, values=[str(i).zfill(2) for i in range(1, 32)], variable=self.day_var,
                        width=60).pack(side="left", padx=2)
        ctk.CTkComboBox(date_frame, values=[str(i).zfill(2) for i in range(1, 13)], variable=self.month_var,
                        width=60).pack(side="left", padx=2)
        ctk.CTkComboBox(date_frame, values=[str(i) for i in range(2020, 2031)], variable=self.year_var, width=80).pack(
            side="left", padx=2)

        # Start Time
        ctk.CTkLabel(card, text="Start Time:", font=("Segoe UI", 20, "bold")).grid(row=3, column=0, sticky="w", padx=20,
                                                                                   pady=12)
        start_frame = ctk.CTkFrame(card, fg_color="transparent")
        start_frame.grid(row=3, column=1, sticky="w", padx=20, pady=12)
        ctk.CTkComboBox(start_frame, values=[str(i).zfill(2) for i in range(1, 13)], variable=self.start_hour_var,
                        width=60).pack(side="left", padx=2)
        ctk.CTkLabel(start_frame, text=":", font=("Segoe UI", 18)).pack(side="left")
        ctk.CTkComboBox(start_frame, values=[str(i).zfill(2) for i in range(0, 60, 5)], variable=self.start_minute_var,
                        width=60).pack(side="left", padx=2)
        ctk.CTkComboBox(start_frame, values=["AM", "PM"], variable=self.start_ampm_var, width=60).pack(side="left",
                                                                                                       padx=2)

        # End Time
        ctk.CTkLabel(card, text="End Time:", font=("Segoe UI", 20, "bold")).grid(row=4, column=0, sticky="w", padx=20,
                                                                                 pady=12)
        end_frame = ctk.CTkFrame(card, fg_color="transparent")
        end_frame.grid(row=4, column=1, sticky="w", padx=20, pady=12)
        ctk.CTkComboBox(end_frame, values=[str(i).zfill(2) for i in range(1, 13)], variable=self.end_hour_var,
                        width=60).pack(side="left", padx=2)
        ctk.CTkLabel(end_frame, text=":", font=("Segoe UI", 18)).pack(side="left")
        ctk.CTkComboBox(end_frame, values=[str(i).zfill(2) for i in range(0, 60, 5)], variable=self.end_minute_var,
                        width=60).pack(side="left", padx=2)
        ctk.CTkComboBox(end_frame, values=["AM", "PM"], variable=self.end_ampm_var, width=60).pack(side="left", padx=2)

        # Buttons
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        ctk.CTkButton(btn_frame, text="ADD ACTIVITY", width=200, height=50, command=self.add_activity_to_database).pack(
            side="left", padx=12)
        ctk.CTkButton(btn_frame, text="VIEW PARTICIPANTS", width=200, height=50, command=self.view_participants).pack(
            side="left", padx=12)
        ctk.CTkButton(btn_frame, text="LOGOUT", width=200, height=50, fg_color="#DC143C", hover_color="#a3001d",
                      command=self.logout).pack(side="left", padx=12)

        # Configure grid
        card.grid_columnconfigure(1, weight=1)

    def convert_to_24hr(self, hour, minute, ampm):
        hour = int(hour)
        minute = int(minute)
        if ampm == "PM" and hour != 12:
            hour += 12
        elif ampm == "AM" and hour == 12:
            hour = 0
        return f"{hour:02d}:{minute:02d}"

    def add_activity_to_database(self):
        # Create database connection for this operation
        conn = None
        try:
            conn = mysql.connector.connect(**DB)
            cursor = conn.cursor()

            name = self.activity_name_var.get().strip()
            club = self.club_name_var.get().strip()
            date_val = f"{self.year_var.get()}-{self.month_var.get()}-{self.day_var.get()}"
            start = self.convert_to_24hr(self.start_hour_var.get(), self.start_minute_var.get(),
                                         self.start_ampm_var.get())
            end = self.convert_to_24hr(self.end_hour_var.get(), self.end_minute_var.get(), self.end_ampm_var.get())

            if not name or not club:
                messagebox.showerror("Error", "All fields are required!")
                return
            if start >= end:
                messagebox.showerror("Error", "End time must be after start time!")
                return

            # Insert into activities table in geccs database
            cursor.execute(
                "INSERT INTO activities (activity_name, club_name, date, time_from, time_to) VALUES (%s,%s,%s,%s,%s)",
                (name, club, date_val, start, end))
            conn.commit()

            messagebox.showinfo("Success", "Activity added successfully!")
            self.clear_fields()

        except mysql.connector.Error as e:
            messagebox.showerror("DB Error", str(e))
        finally:
            if conn:
                conn.close()

    def clear_fields(self):
        self.activity_name_var.set("")
        self.club_name_var.set("")
        now = datetime.now()
        self.day_var.set(str(now.day).zfill(2))
        self.month_var.set(str(now.month).zfill(2))
        self.year_var.set(str(now.year))
        self.start_hour_var.set("09")
        self.start_minute_var.set("00")
        self.start_ampm_var.set("AM")
        self.end_hour_var.set("10")
        self.end_minute_var.set("00")
        self.end_ampm_var.set("AM")

    def view_participants(self):
        self.destroy()
        from student_participation import StudentParticipationApp
        app = StudentParticipationApp()
        app.mainloop()

    def logout(self):
        self.destroy()
        from faculty_login import FacultyLogin
        app = FacultyLogin()
        app.mainloop()


if __name__ == "__main__":
    app = FacultyDashboard()
    app.mainloop()