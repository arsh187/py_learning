import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import webbrowser
import re

# ── Database ────────────────────────────────────────────────────────────────

DB = "placement.db"

def init_db():
    with sqlite3.connect(DB) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS student (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                name  TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)
        con.commit()

def db_add(name, email):
    with sqlite3.connect(DB) as con:
        con.execute("INSERT INTO student (name, email) VALUES (?, ?)", (name, email))
        con.commit()

def db_all():
    with sqlite3.connect(DB) as con:
        return con.execute("SELECT id, name, email FROM student ORDER BY id").fetchall()

def db_count():
    with sqlite3.connect(DB) as con:
        return con.execute("SELECT COUNT(*) FROM student").fetchone()[0]

def db_delete(student_id):
    with sqlite3.connect(DB) as con:
        con.execute("DELETE FROM student WHERE id = ?", (student_id,))
        con.commit()

def db_get_by_email(email):
    with sqlite3.connect(DB) as con:
        return con.execute("SELECT id, name, email FROM student WHERE email = ?", (email,)).fetchone()

def db_update(email, new_name, new_email):
    with sqlite3.connect(DB) as con:
        con.execute("UPDATE student SET name = ?, email = ? WHERE email = ?", (new_name, new_email, email))
        con.commit()

# ── Helpers ─────────────────────────────────────────────────────────────────

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"
COMPANY_URL = "https://www.tcs.com"

def valid_email(e):
    return re.match(r"[^@]+@[^@]+\.[^@]+", e) is not None

# ── Main Application ─────────────────────────────────────────────────────────

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Campus Placement Registration System")
        self.geometry("960x620")
        self.resizable(False, False)
        self.configure(bg="#0f172a")

        self._build_styles()
        self._build_sidebar()
        self._build_content()

        # pages
        self.pages = {}
        for PageClass in (HomePage, AboutPage, RegisterPage,
                          ViewPage, DeletePage, LoginPage, UpdatePage):
            page = PageClass(self.content, self)
            self.pages[PageClass.PAGE_ID] = page
            page.place(relwidth=1, relheight=1)

        self.show("home")

    # ── Styles ───────────────────────────────────────────────────────────────

    def _build_styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("Treeview",
                     background="#1e293b", foreground="#e2e8f0",
                     fieldbackground="#1e293b", rowheight=28,
                     font=("Courier New", 10))
        s.configure("Treeview.Heading",
                     background="#334155", foreground="#94a3b8",
                     font=("Courier New", 10, "bold"))
        s.map("Treeview", background=[("selected", "#3b82f6")])

    # ── Sidebar ──────────────────────────────────────────────────────────────

    def _build_sidebar(self):
        sb = tk.Frame(self, bg="#1e293b", width=200)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        tk.Label(sb, text="📋", font=("Segoe UI Emoji", 28),
                 bg="#1e293b", fg="#3b82f6").pack(pady=(28, 4))
        tk.Label(sb, text="Placement\nPortal", font=("Georgia", 13, "bold"),
                 bg="#1e293b", fg="#f1f5f9", justify="center").pack(pady=(0, 28))

        nav = [
            ("🏠  Home",            "home"),
            ("ℹ️   About",           "about"),
            ("✏️   Register",        "register"),
            ("👥  View Students",   "view"),
            ("🗑️   Delete Student",  "delete"),
            ("🔐  Login",           "login"),
            ("🔄  Update Profile",  "update"),
        ]
        self._nav_buttons = {}
        for label, pid in nav:
            btn = tk.Button(
                sb, text=label, anchor="w", padx=16,
                font=("Courier New", 10), bd=0, cursor="hand2",
                bg="#1e293b", fg="#94a3b8", activebackground="#334155",
                activeforeground="#f1f5f9",
                command=lambda p=pid: self.show(p)
            )
            btn.pack(fill="x", ipady=8)
            self._nav_buttons[pid] = btn

        # total count at bottom
        self.count_var = tk.StringVar()
        self._refresh_count()
        tk.Label(sb, textvariable=self.count_var,
                 font=("Courier New", 9), bg="#1e293b", fg="#475569").pack(side="bottom", pady=16)

    def _build_content(self):
        self.content = tk.Frame(self, bg="#0f172a")
        self.content.pack(side="left", fill="both", expand=True)

    def show(self, page_id):
        for pid, btn in self._nav_buttons.items():
            btn.configure(bg="#1e293b", fg="#94a3b8")
        self._nav_buttons[page_id].configure(bg="#3b82f6", fg="#ffffff")
        self.pages[page_id].tkraise()
        self.pages[page_id].on_show()
        self._refresh_count()

    def _refresh_count(self):
        n = db_count()
        self.count_var.set(f"Total Students: {n}")


# ── Base Page ────────────────────────────────────────────────────────────────

class BasePage(tk.Frame):
    PAGE_ID = ""

    def __init__(self, parent, app):
        super().__init__(parent, bg="#0f172a")
        self.app = app

    def heading(self, title, subtitle=""):
        tk.Label(self, text=title, font=("Georgia", 20, "bold"),
                 bg="#0f172a", fg="#f1f5f9").pack(pady=(36, 2))
        if subtitle:
            tk.Label(self, text=subtitle, font=("Courier New", 10),
                     bg="#0f172a", fg="#64748b").pack(pady=(0, 20))
        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=40, pady=(0, 24))

    def field(self, parent, label, var, show=None):
        tk.Label(parent, text=label, font=("Courier New", 10),
                 bg="#0f172a", fg="#94a3b8", anchor="w").pack(fill="x")
        kw = dict(textvariable=var, font=("Courier New", 11),
                  bg="#1e293b", fg="#e2e8f0", insertbackground="#e2e8f0",
                  relief="flat", bd=0, highlightthickness=1,
                  highlightcolor="#3b82f6", highlightbackground="#334155")
        if show:
            kw["show"] = show
        tk.Entry(parent, **kw).pack(fill="x", ipady=6, pady=(2, 12))

    def btn(self, parent, text, cmd, color="#3b82f6"):
        tk.Button(parent, text=text, command=cmd,
                  font=("Courier New", 10, "bold"), cursor="hand2",
                  bg=color, fg="white", activebackground="#2563eb",
                  activeforeground="white", relief="flat", bd=0
                  ).pack(fill="x", ipady=8, pady=(4, 0))

    def msg(self, text, ok=True):
        color = "#22c55e" if ok else "#ef4444"
        lbl = tk.Label(self, text=text, font=("Courier New", 10),
                       bg="#0f172a", fg=color)
        lbl.pack()
        self.after(3000, lbl.destroy)

    def on_show(self):
        pass


# ── Pages ────────────────────────────────────────────────────────────────────

class HomePage(BasePage):
    PAGE_ID = "home"

    def __init__(self, parent, app):
        super().__init__(parent, app)
        tk.Label(self, text="🎓", font=("Segoe UI Emoji", 56),
                 bg="#0f172a").pack(pady=(60, 8))
        tk.Label(self, text="Campus Placement\nRegistration System",
                 font=("Georgia", 22, "bold"), bg="#0f172a",
                 fg="#f1f5f9", justify="center").pack()
        tk.Label(self, text="Manage student registrations · Track placements · Login to company portal",
                 font=("Courier New", 10), bg="#0f172a", fg="#64748b").pack(pady=(8, 32))

        cards = [
            ("✏️", "Register", "register"),
            ("👥", "View All", "view"),
            ("🔐", "Login", "login"),
        ]
        row = tk.Frame(self, bg="#0f172a")
        row.pack()
        for icon, label, pid in cards:
            card = tk.Frame(row, bg="#1e293b", width=140, height=110, cursor="hand2")
            card.pack(side="left", padx=10, pady=8)
            card.pack_propagate(False)
            tk.Label(card, text=icon, font=("Segoe UI Emoji", 24),
                     bg="#1e293b").pack(pady=(16, 4))
            tk.Label(card, text=label, font=("Courier New", 11, "bold"),
                     bg="#1e293b", fg="#94a3b8").pack()
            card.bind("<Button-1>", lambda e, p=pid: app.show(p))
            for child in card.winfo_children():
                child.bind("<Button-1>", lambda e, p=pid: app.show(p))


class AboutPage(BasePage):
    PAGE_ID = "about"

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.heading("About This System")
        info = [
            ("🎯  Purpose",   "Streamline campus placement registrations and track student data."),
            ("🗄️  Database",   "SQLite3 — lightweight, file-based, zero configuration."),
            ("🖥️  Framework",  "Python Tkinter — native desktop GUI, no internet required."),
            ("🔐  Login",      "Admin login opens the company portal in your browser."),
            ("📊  Features",   "Register · View · Delete · Update profiles · Live student count."),
        ]
        frame = tk.Frame(self, bg="#0f172a")
        frame.pack(padx=60, fill="x")
        for title, desc in info:
            tk.Label(frame, text=title, font=("Courier New", 11, "bold"),
                     bg="#0f172a", fg="#3b82f6", anchor="w").pack(fill="x", pady=(10, 0))
            tk.Label(frame, text=desc, font=("Courier New", 10),
                     bg="#0f172a", fg="#94a3b8", anchor="w", wraplength=600, justify="left"
                     ).pack(fill="x")


class RegisterPage(BasePage):
    PAGE_ID = "register"

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.heading("Register Student", "Add a new student to the placement pool")
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        f = tk.Frame(self, bg="#0f172a")
        f.pack(padx=120, fill="x")
        self.field(f, "Full Name", self.name_var)
        self.field(f, "Email Address", self.email_var)
        self.btn(f, "Register Student", self._register)

    def _register(self):
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        if not name or not email:
            self.msg("All fields are required.", ok=False); return
        if not valid_email(email):
            self.msg("Enter a valid email address.", ok=False); return
        try:
            db_add(name, email)
            self.name_var.set("")
            self.email_var.set("")
            self.msg(f"✅  {name} registered successfully!")
            self.app._refresh_count()
        except sqlite3.IntegrityError:
            self.msg("Email already registered.", ok=False)


class ViewPage(BasePage):
    PAGE_ID = "view"

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.heading("Registered Students")
        cols = ("ID", "Name", "Email")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=16)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=220 if c != "ID" else 60, anchor="center" if c == "ID" else "w")
        self.tree.pack(padx=40, fill="x")

    def on_show(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in db_all():
            self.tree.insert("", "end", values=row)


class DeletePage(BasePage):
    PAGE_ID = "delete"

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.heading("Delete Student", "Select a student and remove them from the system")
        cols = ("ID", "Name", "Email")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=12)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=220 if c != "ID" else 60, anchor="center" if c == "ID" else "w")
        self.tree.pack(padx=40, fill="x")
        f = tk.Frame(self, bg="#0f172a")
        f.pack(padx=40, fill="x", pady=12)
        self.btn(f, "🗑️  Delete Selected Student", self._delete, color="#ef4444")

    def on_show(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in db_all():
            self.tree.insert("", "end", values=row)

    def _delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Select a student first."); return
        vals = self.tree.item(sel[0], "values")
        if messagebox.askyesno("Confirm", f"Delete {vals[1]} ({vals[2]})?"):
            db_delete(vals[0])
            self.on_show()
            self.app._refresh_count()
            self.msg(f"Deleted {vals[1]}.")


class LoginPage(BasePage):
    PAGE_ID = "login"

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.heading("Admin Login", "Authenticate to open the company portal")
        self.user_var = tk.StringVar()
        self.pass_var = tk.StringVar()
        f = tk.Frame(self, bg="#0f172a")
        f.pack(padx=160, fill="x")
        self.field(f, "Username", self.user_var)
        self.field(f, "Password", self.pass_var, show="•")
        self.btn(f, "Login & Open Company Portal", self._login)
        tk.Label(f, text="Default credentials: admin / admin123",
                 font=("Courier New", 9), bg="#0f172a", fg="#475569").pack(pady=(8, 0))

    def _login(self):
        u = self.user_var.get().strip()
        p = self.pass_var.get().strip()
        if u == ADMIN_USER and p == ADMIN_PASS:
            self.msg("✅  Login successful! Opening company portal…")
            self.user_var.set("")
            self.pass_var.set("")
            self.after(800, lambda: webbrowser.open(COMPANY_URL))
        else:
            self.msg("Invalid credentials.", ok=False)


class UpdatePage(BasePage):
    PAGE_ID = "update"

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.heading("Update Profile", "Look up a student by email and update their details")

        self.search_var = tk.StringVar()
        self.new_name_var = tk.StringVar()
        self.new_email_var = tk.StringVar()

        f = tk.Frame(self, bg="#0f172a")
        f.pack(padx=120, fill="x")

        # Search section
        tk.Label(f, text="Current Email (to search)", font=("Courier New", 10),
                 bg="#0f172a", fg="#94a3b8", anchor="w").pack(fill="x")
        row = tk.Frame(f, bg="#0f172a")
        row.pack(fill="x", pady=(2, 12))
        tk.Entry(row, textvariable=self.search_var, font=("Courier New", 11),
                 bg="#1e293b", fg="#e2e8f0", insertbackground="#e2e8f0",
                 relief="flat", bd=0, highlightthickness=1,
                 highlightcolor="#3b82f6", highlightbackground="#334155"
                 ).pack(side="left", fill="x", expand=True, ipady=6)
        tk.Button(row, text="  Find  ", command=self._find,
                  font=("Courier New", 10, "bold"), cursor="hand2",
                  bg="#334155", fg="#f1f5f9", relief="flat", bd=0
                  ).pack(side="left", padx=(6, 0))

        # Update section
        self.update_frame = tk.Frame(f, bg="#0f172a")
        self.update_frame.pack(fill="x")
        self.field(self.update_frame, "New Name", self.new_name_var)
        self.field(self.update_frame, "New Email", self.new_email_var)
        self.btn(self.update_frame, "Update Profile", self._update)
        self._found_email = None

    def _find(self):
        email = self.search_var.get().strip()
        row = db_get_by_email(email)
        if row:
            self._found_email = email
            self.new_name_var.set(row[1])
            self.new_email_var.set(row[2])
            self.msg(f"Found: {row[1]}")
        else:
            self._found_email = None
            self.msg("No student with that email.", ok=False)

    def _update(self):
        if not self._found_email:
            self.msg("Search for a student first.", ok=False); return
        new_name = self.new_name_var.get().strip()
        new_email = self.new_email_var.get().strip()
        if not new_name or not new_email:
            self.msg("Fields cannot be empty.", ok=False); return
        if not valid_email(new_email):
            self.msg("Enter a valid email.", ok=False); return
        try:
            db_update(self._found_email, new_name, new_email)
            self._found_email = new_email
            self.msg("✅  Profile updated successfully!")
            self.app._refresh_count()
        except sqlite3.IntegrityError:
            self.msg("That email is already in use.", ok=False)


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    app = App()
    app.mainloop()
