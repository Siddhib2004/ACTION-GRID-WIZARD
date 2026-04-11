import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector
import csv
from datetime import datetime

# ---------- DB CONFIG ----------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "geccs"
}
# --------------------------------

def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Cannot connect to DB:\n{e}")
        return None

class StudentRecordViewer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Student Activity Record")
        self.geometry("1000*600")
        self.minsize(1400, 600)
        #self.resizable(True, True)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.enrollment_var = ctk.StringVar()
        self._build_ui()

    def _build_ui(self):
        # Header
        ctk.CTkLabel(self, text="Student Activity Record", font=("Segoe UI", 24, "bold")).pack(pady=12)

        # Input + Fetch
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(input_frame, text="Enrollment No:", font=("Segoe UI", 14)).pack(side="left", padx=8)
        self.enroll_entry = ctk.CTkEntry(input_frame, textvariable=self.enrollment_var, width=250)
        self.enroll_entry.pack(side="left", padx=8)
        self.enroll_entry.bind("<Return>", lambda e: self.fetch_activities())

        ctk.CTkButton(input_frame, text="FETCH ACTIVITIES", command=self.fetch_activities, width=180).pack(side="left", padx=8)

        # Table
        table_frame = ctk.CTkFrame(self, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        cols = ("Activity", "Date", "Time From", "Time To", "Role")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=200, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(table_frame, orientation="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Bottom buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=12)

        ctk.CTkButton(btn_frame, text="EXPORT CSV", width=140, command=self.export_to_csv).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="PRINT", width=140, command=self.print_record).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="BACK", width=120, fg_color="#6c757d", command=self.destroy).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="EXIT", width=120, fg_color="#dc3545", command=self.exit_app).pack(side="left", padx=10)

    # ---------- DB / Logic ----------
    def fetch_activities(self):
        enrollment = self.enrollment_var.get().strip()
        if not enrollment:
            messagebox.showwarning("Warning", "Please enter Enrollment Number")
            return

        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("""SELECT activity_name, activity_date, time_from, time_to, role 
                           FROM participation WHERE enrollment_no=%s ORDER BY activity_date DESC""", (enrollment,))
            rows = cur.fetchall()
            if not rows:
                messagebox.showinfo("No Records", f"No activities found for {enrollment}")
                return
            for r in rows:
                self.tree.insert("", "end", values=[r[0], r[1], str(r[2])[:5], str(r[3])[:5], r[4]])
        except mysql.connector.Error as e:
            messagebox.showerror("DB Error", str(e))
        finally:
            conn.close()

    def export_to_csv(self):
        if not self.tree.get_children():
            messagebox.showwarning("No Data", "No activities to export")
            return
        enrollment = self.enrollment_var.get().strip()
        filename = f"activities_{enrollment}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        try:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([self.tree.heading(c)["text"] for c in self.tree["columns"]])
                for item in self.tree.get_children():
                    writer.writerow(self.tree.item(item)["values"])
            messagebox.showinfo("Exported", f"CSV saved as {filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def print_record(self):
        messagebox.showinfo("Print", "This would print the student record (simulated).")

    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.destroy()

# ---------- Run ----------
if __name__ == "__main__":
    app = StudentRecordViewer()
    app.mainloop()
