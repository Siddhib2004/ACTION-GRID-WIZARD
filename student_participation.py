# student_participation.py
import os
import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error, IntegrityError

# UI appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ---------- CONFIG: change these to match your MySQL setup ----------
LOGO_PATH = ""  # optional logo path
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # set if needed
    "database": "geccs"  # your database name
}


# -----------------------------------------------------------------------

def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        messagebox.showerror("Database Error", f"Could not connect to DB:\n{e}")
        return None


class StudentParticipationApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GECCS Activity System - Student Participation")
        self.geometry("1000x600")
        self.minsize(1400, 600)
        self.resizable(True, True)
        self.configure(fg_color="#F7F7F7")

        self._build_ui()
        self._center()
        self.load_activities()  # populate activities dropdown on start

    def _center(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=14)
        ctk.CTkLabel(header, text="Student Participation",
                     font=("Segoe UI", 24, "bold"),
                     text_color="#003333").pack(side="left", padx=16)

        # Main card
        card = ctk.CTkFrame(self, width=1100, height=620, corner_radius=14)
        card.pack(pady=10)
        card.pack_propagate(False)

        # Left: form area
        form_frame = ctk.CTkFrame(card, fg_color="transparent")
        form_frame.place(relx=0.02, rely=0.02, relwidth=0.46, relheight=0.96)

        LABEL_FONT = ("Segoe UI", 14)
        ENTRY_W = 360
        PADY = 10

        # Enrollment No (auto-fetch on focus out)
        ctk.CTkLabel(form_frame, text="Enrollment No", font=LABEL_FONT).grid(row=0, column=0, sticky="w", padx=8,
                                                                             pady=(18, PADY))
        self.enrollment_entry = ctk.CTkEntry(form_frame, width=ENTRY_W, placeholder_text="Enter enrollment no")
        self.enrollment_entry.grid(row=0, column=1, padx=8, pady=(18, PADY))
        self.enrollment_entry.bind("<FocusOut>", lambda e: self.fetch_student_details())

        # Student Name
        ctk.CTkLabel(form_frame, text="Student Name", font=LABEL_FONT).grid(row=1, column=0, sticky="w", padx=8,
                                                                            pady=PADY)
        self.name_entry = ctk.CTkEntry(form_frame, width=ENTRY_W)
        self.name_entry.grid(row=1, column=1, padx=8, pady=PADY)

        # Department
        ctk.CTkLabel(form_frame, text="Department", font=LABEL_FONT).grid(row=2, column=0, sticky="w", padx=8,
                                                                          pady=PADY)
        self.dept_menu = ctk.CTkOptionMenu(form_frame,
                                           values=["CSE", "IT", "ENTC", "EEE", "MECH", "CIVIL", "AUTO"],
                                           width=ENTRY_W)
        self.dept_menu.set("Select")
        self.dept_menu.grid(row=2, column=1, padx=8, pady=PADY)

        # Class
        ctk.CTkLabel(form_frame, text="Class", font=LABEL_FONT).grid(row=3, column=0, sticky="w", padx=8, pady=PADY)
        self.class_entry = ctk.CTkEntry(form_frame, width=ENTRY_W)
        self.class_entry.grid(row=3, column=1, padx=8, pady=PADY)

        # Activity dropdown
        ctk.CTkLabel(form_frame, text="Activity", font=LABEL_FONT).grid(row=4, column=0, sticky="w", padx=8, pady=PADY)
        self.activity_dropdown = ctk.CTkOptionMenu(form_frame, values=[], width=ENTRY_W)
        self.activity_dropdown.set("")  # start empty
        self.activity_dropdown.grid(row=4, column=1, padx=8, pady=PADY)
        self.activity_dropdown.configure(command=self.fetch_activity_details)

        # Activity date/time fields
        ctk.CTkLabel(form_frame, text="Activity Date", font=LABEL_FONT).grid(row=5, column=0, sticky="w", padx=8,
                                                                             pady=PADY)
        self.act_date = ctk.CTkEntry(form_frame, width=ENTRY_W)
        self.act_date.grid(row=5, column=1, padx=8, pady=PADY)

        ctk.CTkLabel(form_frame, text="Time From", font=LABEL_FONT).grid(row=6, column=0, sticky="w", padx=8, pady=PADY)
        self.time_from = ctk.CTkEntry(form_frame, width=ENTRY_W)
        self.time_from.grid(row=6, column=1, padx=8, pady=PADY)

        ctk.CTkLabel(form_frame, text="Time To", font=LABEL_FONT).grid(row=7, column=0, sticky="w", padx=8, pady=PADY)
        self.time_to = ctk.CTkEntry(form_frame, width=ENTRY_W)
        self.time_to.grid(row=7, column=1, padx=8, pady=PADY)

        # Club Name (fetched from activities table)
        ctk.CTkLabel(form_frame, text="Club Name", font=LABEL_FONT).grid(row=8, column=0, sticky="w", padx=8, pady=PADY)
        self.club_name_entry = ctk.CTkEntry(form_frame, width=ENTRY_W, state="readonly")
        self.club_name_entry.grid(row=8, column=1, padx=8, pady=PADY)

        # Role
        ctk.CTkLabel(form_frame, text="Role", font=LABEL_FONT).grid(row=9, column=0, sticky="w", padx=8, pady=PADY)
        self.role_menu = ctk.CTkOptionMenu(form_frame, values=["Participant", "Head Coordinator", "Coordinator"],
                                           width=ENTRY_W)
        self.role_menu.set("Participant")
        self.role_menu.grid(row=9, column=1, padx=8, pady=PADY)

        # Buttons
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=10, column=0, columnspan=2, pady=18)

        self.add_btn = ctk.CTkButton(btn_frame, text="Add Student", width=160, fg_color="#007ACC",
                                     command=self.add_student_to_table)
        self.add_btn.grid(row=0, column=0, padx=8)
        self.save_btn = ctk.CTkButton(btn_frame, text="Save Participation", width=200, fg_color="#0A66C2",
                                      command=self.save_participation)
        self.save_btn.grid(row=0, column=1, padx=8)
        self.view_btn = ctk.CTkButton(btn_frame, text="Student Record", width=100, fg_color="#1070D6",
                                      command=self.open_student_records)
        self.view_btn.grid(row=0, column=2, padx=10)

        # NEW: View Record button added before Back button
        self.view_record_btn = ctk.CTkButton(btn_frame, text="View Record", width=160, fg_color="#1070D6",
                                             command=self.open_student_records)
        self.view_record_btn.grid(row=1, column=0, padx=8, pady=8)

        self.back_btn = ctk.CTkButton(btn_frame, text="Back To Dashboard", width=200, fg_color="#1070D6",
                                      command=self.back_to_dashboard)
        self.back_btn.grid(row=1, column=1, padx=8, pady=8)

        # Right: Table
        table_frame = ctk.CTkFrame(card, fg_color="transparent")
        table_frame.place(relx=0.50, rely=0.02, relwidth=0.48, relheight=0.96)

        cols = ("Enrollment No", "Name", "Department", "Class", "Activity", "Date", "Time From", "Time To", "Club",
                "Role")
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"))
        style.configure("Treeview", font=("Segoe UI", 11), rowheight=30)

        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            w = 120 if c not in ["Name", "Activity"] else 150
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor="w")

        ysb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        xsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
        self.tree.pack(side="top", fill="both", expand=True, padx=6, pady=6)
        ysb.pack(side="right", fill="y")
        xsb.pack(side="bottom", fill="x")

    # --------- DB / UI logic ----------
    def fetch_student_details(self):
        enrollment = self.enrollment_entry.get().strip()
        if not enrollment:
            return
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT name, department, class FROM students WHERE enrollment_no = %s", (enrollment,))
            row = cur.fetchone()
            if row:
                self.name_entry.delete(0, "end");
                self.name_entry.insert(0, row[0])
                try:
                    self.dept_menu.set(row[1])
                except:
                    self.dept_menu.set(row[1])
                self.class_entry.delete(0, "end");
                self.class_entry.insert(0, row[2])
            else:
                messagebox.showwarning("Not found", "Student not found for this Enrollment No.")
                self.name_entry.delete(0, "end");
                self.dept_menu.set("Select");
                self.class_entry.delete(0, "end")
        except Error as e:
            messagebox.showerror("DB Error", str(e))
        finally:
            conn.close()

    def load_activities(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT activity_name FROM activities ORDER BY activity_name")
            rows = cur.fetchall()
            values = [r[0] for r in rows]
            self.activity_dropdown.configure(values=values)
            if values:
                self.activity_dropdown.set(values[0])
            else:
                self.activity_dropdown.set("")
        except Error as e:
            messagebox.showerror("DB Error", str(e))
        finally:
            conn.close()

    def fetch_activity_details(self, activity_name):
        if not activity_name:
            return
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT date, time_from, time_to, club_name FROM activities WHERE activity_name = %s",
                        (activity_name,))
            row = cur.fetchone()
            if row:
                self.act_date.delete(0, "end");
                self.act_date.insert(0, str(row[0]))
                self.time_from.delete(0, "end");
                self.time_from.insert(0, str(row[1]))
                self.time_to.delete(0, "end");
                self.time_to.insert(0, str(row[2]))
                self.club_name_entry.configure(state="normal")
                self.club_name_entry.delete(0, "end");
                self.club_name_entry.insert(0, str(row[3]))
                self.club_name_entry.configure(state="readonly")
            else:
                self.act_date.delete(0, "end");
                self.time_from.delete(0, "end");
                self.time_to.delete(0, "end")
                self.club_name_entry.configure(state="normal")
                self.club_name_entry.delete(0, "end")
                self.club_name_entry.configure(state="readonly")
        except Error as e:
            messagebox.showerror("DB Error", str(e))
        finally:
            conn.close()

    def add_student_to_table(self):
        enr = self.enrollment_entry.get().strip()
        name = self.name_entry.get().strip()
        dept = self.dept_menu.get()
        cls = self.class_entry.get().strip()
        activity = self.activity_dropdown.get()
        date = self.act_date.get().strip()
        tfrom = self.time_from.get().strip()
        tto = self.time_to.get().strip()
        club = self.club_name_entry.get().strip()
        role = self.role_menu.get()

        if not enr or not name:
            messagebox.showerror("Missing", "Please enter Enrollment and fetch student details.")
            return
        if not activity or not date:
            messagebox.showerror("Missing", "Please choose an activity.")
            return

        for iid in self.tree.get_children():
            vals = self.tree.item(iid)["values"]
            if vals[0] == enr and vals[4] == activity:
                messagebox.showerror("Duplicate", "This student is already added for the same activity.")
                return

        self.tree.insert("", "end", values=(enr, name, dept, cls, activity, date, tfrom, tto, club, role))
        self.enrollment_entry.delete(0, "end")
        self.name_entry.delete(0, "end")
        self.dept_menu.set("Select")
        self.class_entry.delete(0, "end")
        self.enrollment_entry.focus_set()

    def save_participation(self):
        items = self.tree.get_children()
        if not items:
            messagebox.showwarning("No data", "No rows to save.")
            return
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            q = """INSERT INTO participation
                   (enrollment_no, name, department, class, activity_name, activity_date, time_from, time_to, club_name, \
                    role)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            saved = 0
            errors = []
            for iid in list(items):
                vals = self.tree.item(iid)["values"]
                try:
                    cur.execute(q, tuple(vals))
                    saved += 1
                    self.tree.delete(iid)
                except IntegrityError as ie:
                    errors.append(f"Duplicate: {vals[0]} -> {vals[4]}")
                except Error as e:
                    errors.append(f"Error for {vals[0]}: {str(e)}")
            conn.commit()
            if saved: messagebox.showinfo("Saved", f"{saved} record(s) saved.")
            if errors: messagebox.showwarning("Partial Save / Errors", "\n".join(errors))
        except Error as e:
            messagebox.showerror("DB Error", str(e))
            conn.rollback()
        finally:
            conn.close()

    def open_student_records(self):
        self.destroy()
        from student_record import StudentRecordViewer
        app = StudentRecordViewer()
        app.mainloop()

    def back_to_dashboard(self):
        self.destroy()
        from faculty_dashboard import FacultyDashboard
        app = FacultyDashboard()
        app.mainloop()


class StudentRecordWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Student Participation Records")
        self.geometry("900x500")
        self.transient(parent)
        self.grab_set()

        ctk.CTkLabel(self, text="Participation Records", font=("Segoe UI", 18, "bold")).pack(pady=12)

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=12, pady=8)

        cols = ("Enrollment No", "Name", "Department", "Activity", "Date", "Club", "Role")
        style = ttk.Style()
        style.configure("Record.Treeview", font=("Segoe UI", 11), rowheight=28)

        self.tree = ttk.Treeview(frame, columns=cols, show="headings", style="Record.Treeview")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=140, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)

        ysb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=ysb.set)
        ysb.pack(side="right", fill="y")

        # Load records
        self.load_records()
        ctk.CTkButton(self, text="Close", width=140, fg_color="#6c757d", command=self.destroy).pack(pady=8)

    def load_records(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""SELECT enrollment_no, name, department, activity_name, activity_date, club_name, role
                           FROM participation
                           ORDER BY activity_date DESC""")
            for row in cur.fetchall():
                self.tree.insert("", "end", values=row)
        except Error as e:
            messagebox.showerror("DB Error", str(e))
        finally:
            conn.close()


if __name__ == "__main__":
    app = StudentParticipationApp()
    app.mainloop()