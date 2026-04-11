

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import mysql.connector

# ---------- Config ----------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
DB = dict(host="localhost", user="root", password="", database="geccs")

DEPARTMENTS = ["ENTC","CSE", "IT", "EEE", "MECH", "CIVIL", "AUTO"]
CLASSES = ["FY", "SY", "TY","BE"]

# ---------- Helpers ----------
def db_connect():
    try:
        return mysql.connector.connect(**DB)
    except mysql.connector.Error as e:
        messagebox.showerror("DB Error", str(e))
        return None

# ---------- App ----------
class AdminDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Admin Dashboard — Student Data Entry")
        self.geometry("1400*600")
        self.minsize(1400, 600)

        self._editor = None
        self._editor_item = None
        self._editor_col = None

        self._build_ui()

    def _build_ui(self):
        # Header (centered, Fluent style)
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(18, 6))

        ctk.CTkLabel(header, text="GECCS", font=("Segoe UI", 20, "bold"), text_color="#0B3D3E").pack(side="left", padx=24)
        ctk.CTkLabel(header, text="Student Data Entry", font=("Segoe UI", 34, "bold"), text_color="#0A66C2").pack(side="left", padx=12)
        ctk.CTkLabel(header, text="(Admin)", font=("Segoe UI", 16), text_color="#5a6b76").pack(side="left", padx=8)

        # Separator
        sep = ttk.Separator(self, orient="horizontal")
        sep.pack(fill="x", padx=24, pady=(6, 12))

        # Card container
        card = ctk.CTkFrame(self, corner_radius=14, fg_color="white")
        card.pack(fill="both", expand=True, padx=24, pady=12)

        # Tree area
        self._build_table(card)

        # Buttons
        btns = ctk.CTkFrame(card, fg_color="transparent")
        btns.pack(pady=18)
        ctk.CTkButton(btns, text="Add Row", width=180, height=48,
                      fg_color="#1070D6", hover_color="#0b5fb0",
                      command=self.add_row, font=("Segoe UI", 16, "bold")).grid(row=0, column=0, padx=12)
        ctk.CTkButton(btns, text="Submit to Database", width=260, height=48,
                      fg_color="#0A66C2", hover_color="#085aa6",
                      command=self.submit, font=("Segoe UI", 16, "bold")).grid(row=0, column=1, padx=12)
        ctk.CTkButton(btns, text="Back", width=160, height=48,
                      fg_color="#8B0000", hover_color="#6e0000",
                      command=self.back, font=("Segoe UI", 16, "bold")).grid(row=0, column=2, padx=12)

    def _build_table(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=18, pady=12)

        cols = ["Academic Year", "Student Name", "Enrollment No", "Department", "Class"]
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 18, "bold"))
        style.configure("Treeview", font=("Segoe UI", 16), rowheight=42)

        self.tree = ttk.Treeview(frame, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            w = 280 if c != "Student Name" else 380
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor=tk.W)

        ysb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        xsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
        self.tree.pack(side="top", fill="both", expand=True)
        ysb.pack(side="right", fill="y")
        xsb.pack(side="bottom", fill="x")

        # Bindings:
        # double-click starts edit
        self.tree.bind("<Double-1>", self._on_double)
        # single-click opens dropdown immediately for Dept/Class
        self.tree.bind("<ButtonRelease-1>", self._on_single_click)

    # ---------------- actions ----------------
    def add_row(self):
        # default sensible values for dropdowns
        self.tree.insert("", "end", values=("", "", "", DEPARTMENTS[0], CLASSES[0]))

    def _on_double(self, e):
        # edit any cell on double-click
        self._start_edit(e, force_entry=True)

    def _on_single_click(self, e):
        # open combobox immediately for Dept/Class on single click
        region = self.tree.identify("region", e.x, e.y)
        if region != "cell":
            return
        col = int(self.tree.identify_column(e.x).replace("#", "")) - 1
        col_name = self.tree["columns"][col]
        if col_name in ("Department", "Class"):
            self._start_edit(e, force_entry=False )

    def _start_edit(self, event, force_entry=False):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        iid = self.tree.identify_row(event.y)
        col = int(self.tree.identify_column(event.x).replace("#", "")) - 1
        col_name = self.tree["columns"][col]
        x, y, w, h = self.tree.bbox(iid, f"#{col+1}")
        old = self.tree.set(iid, col_name)

        # destroy existing editor
        if self._editor:
            self._editor.destroy()
            self._editor = None

        parent = self.tree

        if (col_name in ("Department", "Class")) and not force_entry:
            vals = DEPARTMENTS if col_name == "Department" else CLASSES
            editor = ttk.Combobox(parent, values=vals, state="readonly", font=("Segoe UI", 15))
            editor.set(old if old else vals[0])
            # auto-open dropdown
            editor.pack_forget()  # ensure widget is realized before event_generate
            editor.place(x=x, y=y, width=w, height=h)
            editor.event_generate("<Button-1>")
        else:
            editor = ttk.Entry(parent, font=("Segoe UI", 15))
            editor.insert(0, old)
            editor.place(x=x, y=y, width=w, height=h)

        editor.focus_set()

        def commit(event=None):
            try:
                new = editor.get()
            except Exception:
                new = ""
            self.tree.set(iid, col_name, new)
            editor.destroy()
            self._editor = None

        def cancel(event=None):
            editor.destroy()
            self._editor = None

        editor.bind("<Return>", commit)
        editor.bind("<FocusOut>", commit)
        editor.bind("<Escape>", cancel)
        self._editor = editor
        self._editor_item = iid
        self._editor_col = col_name

    def submit(self):
        # commit any editor
        if self._editor:
            self._editor.destroy()
            self._editor = None

        rows = []
        for iid in self.tree.get_children():
            vals = list(self.tree.item(iid)["values"])
            # ensure length and strip
            vals = [str(v).strip() if v is not None else "" for v in vals]
            # require name and enrollment
            if not vals[1] or not vals[2]:
                continue
            rows.append(tuple(vals[:5]))

        if not rows:
            messagebox.showwarning("No Data", "No valid rows to submit (name & enrollment required).")
            return

        conn = db_connect()
        if not conn:
            return
        try:
            cur = conn.cursor()
            q = "INSERT INTO students (academic_year, name, enrollment_no, department, class) VALUES (%s,%s,%s,%s,%s)"
            cur.executemany(q, rows)
            conn.commit()
            inserted = cur.rowcount
            messagebox.showinfo("Success", f"{inserted} record(s) inserted.")
            # delete inserted rows
            for iid in list(self.tree.get_children()):
                vals = self.tree.item(iid)["values"]
                if vals[1] and vals[2]:
                    self.tree.delete(iid)
        except mysql.connector.IntegrityError as ie:
            messagebox.showerror("DB Integrity", str(ie))
        except mysql.connector.Error as e:
            messagebox.showerror("DB Error", str(e))
        finally:
            conn.close()

    from admin_login import AdminLogin  # <<--- make sure class name matches
    def back(self):
        self.destroy()
        from admin_login import AdminLogin
        app=AdminLogin()
        app.mainloop()
# ---------- Run ----------
if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()
