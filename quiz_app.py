import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random

DB_FILE = "course_questions.db"

COURSE_TABLES = {
    "Management Information Systems": "DS_3841",
    "Business Applications Development": "DS_3850",
    "BI & Analytics Capstone": "DS_4510",
    "Managerial Finance": "FIN_3210"
}

class QuizApp:
    def __init__(self, root, return_to_main=None):
        self.return_to_main = return_to_main
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("600x400")
        self.score = 0
        self.current_question_index = 0
        self.questions = []
        self.welcome_screen()

    def welcome_screen(self):
        # ensure back functionality is preserved
        self.clear_screen()
        tk.Label(self.root, text="Welcome to the Quiz App", font=("Arial", 18)).pack(pady=20)
        tk.Label(self.root, text="Select a Quiz Category:").pack(pady=10)

        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(self.root, textvariable=self.category_var, state="readonly")
        self.category_combo["values"] = list(COURSE_TABLES.keys())
        self.category_combo.pack(pady=10)

        tk.Button(self.root, text="Start Quiz", command=self.load_questions).pack(pady=10)
        if self.return_to_main:
            tk.Button(self.root, text="Back", command=self.return_to_main).pack(pady=5)

    def load_questions(self):
        category_name = self.category_var.get()
        if not category_name:
            messagebox.showwarning("Required", "Please select a category.")
            return

        table_name = COURSE_TABLES[category_name]

        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT question_text, option_a, option_b, option_c, option_d, correct_answer FROM {table_name}")
                rows = cursor.fetchall()
                if not rows:
                    messagebox.showinfo("No Questions", "No questions available in this category.")
                    return
                self.questions = random.sample(rows, min(len(rows), 10))  # pick up to 10 questions
                self.score = 0
                self.current_question_index = 0
                self.quiz_screen()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def quiz_screen(self):
        self.clear_screen()

        if self.current_question_index >= len(self.questions):
            self.show_score()
            return

        q_data = self.questions[self.current_question_index]
        question_text, *options, self.correct_answer = q_data

        tk.Label(self.root, text=f"Question {self.current_question_index + 1}", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text=question_text, wraplength=550).pack(pady=5)

        self.selected_option = tk.StringVar()

        for i, option in zip("ABCD", options):
            tk.Radiobutton(self.root, text=option, variable=self.selected_option, value=i).pack(anchor="w")

        tk.Button(self.root, text="Submit", command=self.check_answer).pack(pady=10)

    def check_answer(self):
        selected = self.selected_option.get()
        if not selected:
            messagebox.showwarning("Select an answer", "Please select an answer before submitting.")
            return

        if selected == self.correct_answer:
            self.score += 1
            messagebox.showinfo("Correct", "✅ That's correct!")
        else:
            messagebox.showinfo("Incorrect", f"❌ Wrong. Correct answer was: {self.correct_answer}")

        self.current_question_index += 1
        self.quiz_screen()

    def show_score(self):
        self.clear_screen()
        tk.Label(self.root, text="Quiz Complete!", font=("Arial", 18)).pack(pady=20)
        tk.Label(self.root, text=f"Your Score: {self.score} / {len(self.questions)}", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="Take Another Quiz", command=self.welcome_screen).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=5)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
