import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import database_questions  # Ensure this creates the DB on first run

DB_FILE = "course_questions.db"
ADMIN_PASSWORD = "admin123"

# Course options dropdown
COURSE_TABLES = {
    "DS_3841": "Mgmt_Information_Systems",
    "DS_3850": "Business_Applications_Develop",
    "DS_4510": "Bus_Intel_Analytics_Capstone",
    "FIN_3210": "Principles_Managerial_Fin"
}


class AdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Login")
        self.root.geometry("500x500")
        self.login_screen()

    def login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Admin Login", font=("Arial", 18)).pack(pady=20)
        tk.Label(self.root, text="Password:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=10)
        tk.Button(self.root, text="Login", command=self.check_login).pack(pady=10)

    def check_login(self):
        if self.password_entry.get() == ADMIN_PASSWORD:
            self.dashboard()
        else:
            messagebox.showerror("Access Denied", "Incorrect password.")

    def dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text="Admin Dashboard", font=("Arial", 18)).pack(pady=20)
        tk.Button(self.root, text="Add New Question", width=25, command=self.add_question_screen).pack(pady=5)
        tk.Button(self.root, text="View/Edit/Delete Questions", width=25, command=self.view_questions_screen).pack(pady=5)
        tk.Button(self.root, text="Logout", width=25, command=self.login_screen).pack(pady=20)

    def add_question_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Add Question", font=("Arial", 16)).pack(pady=10)

        self.course_var = tk.StringVar()
        tk.Label(self.root, text="Course Table").pack()
        self.course_dropdown = ttk.Combobox(self.root, textvariable=self.course_var, values=list(COURSE_TABLES.keys()))
        self.course_dropdown.pack(pady=5)

        fields = ["Question", "Option A", "Option B", "Option C", "Option D", "Correct Answer (A/B/C/D)"]
        self.entries = {}
        for field in fields:
            tk.Label(self.root, text=field).pack()
            entry = tk.Entry(self.root)
            entry.pack(pady=2)
            self.entries[field] = entry

        tk.Button(self.root, text="Submit", command=self.save_question).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.dashboard).pack()

    def save_question(self):
        course_table = self.course_var.get()
        if not course_table:
            messagebox.showerror("Missing Info", "Please select a course.")
            return

        data = {k: v.get() for k, v in self.entries.items()}
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute(f"""
                    INSERT INTO {course_table} (question_text, option_a, option_b, option_c, option_d, correct_answer)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (data["Question"], data["Option A"], data["Option B"],
                     data["Option C"], data["Option D"], data["Correct Answer (A/B/C/D)"])
                )
                conn.commit()
            messagebox.showinfo("Success", "Question added successfully!")
            self.dashboard()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_questions_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="View/Edit/Delete Questions", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Course Table:").pack()
        self.table_var = tk.StringVar()
        self.table_dropdown = ttk.Combobox(self.root, textvariable=self.table_var, values=list(COURSE_TABLES.keys()))
        self.table_dropdown.pack(pady=5)

        tk.Button(self.root, text="Load Questions", command=self.load_questions).pack(pady=5)

        self.tree = ttk.Treeview(self.root, columns=("ID", "Question", "Answer"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Question", text="Question")
        self.tree.heading("Answer", text="Answer")
        self.tree.pack(expand=True, fill="both", pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Edit Selected", command=self.edit_question).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_question).grid(row=0, column=1, padx=5)
        tk.Button(self.root, text="Back", command=self.dashboard).pack(pady=10)

    def load_questions(self):
        table = self.table_var.get()
        if not table:
            messagebox.showerror("Missing Info", "Please select a course.")
            return

        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT id, question_text, correct_answer FROM {table}")
                rows = cursor.fetchall()
                self.tree.delete(*self.tree.get_children())
                for row in rows:
                    self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_question(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a question to delete.")
            return

        item = self.tree.item(selected[0])
        qid = item["values"][0]
        table = self.table_var.get()
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this question?")
        if confirm:
            try:
                with sqlite3.connect(DB_FILE) as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"DELETE FROM {table} WHERE id = ?", (qid,))
                    conn.commit()
                self.load_questions()
                messagebox.showinfo("Deleted", "Question deleted.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def edit_question(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a question to edit.")
            return

        item = self.tree.item(selected[0])
        qid = item["values"][0]
        table = self.table_var.get()

        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute(f"""
                    SELECT question_text, option_a, option_b, option_c, option_d, correct_answer 
                    FROM {table} WHERE id = ?
                """, (qid,))
                question_data = cursor.fetchone()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        # Create popup
        edit_win = tk.Toplevel(self.root)
        edit_win.title("Edit Question")
        edit_win.geometry("400x400")

        labels = ["Question", "Option A", "Option B", "Option C", "Option D", "Correct Answer (A/B/C/D)"]
        self.edit_entries = {}

        for i, label in enumerate(labels):
            tk.Label(edit_win, text=label).pack()
            entry = tk.Entry(edit_win)
            entry.pack(pady=2)
            entry.insert(0, question_data[i])
            self.edit_entries[label] = entry

        def save_changes():
            updated = [self.edit_entries[label].get() for label in labels]
            try:
                with sqlite3.connect(DB_FILE) as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"""
                        UPDATE {table}
                        SET question_text=?, option_a=?, option_b=?, option_c=?, option_d=?, correct_answer=?
                        WHERE id=?
                    """, (*updated, qid))
                    conn.commit()
                messagebox.showinfo("Success", "Question updated.")
                edit_win.destroy()
                self.load_questions()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(edit_win, text="Save Changes", command=save_changes).pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = AdminApp(root)
    root.mainloop()
