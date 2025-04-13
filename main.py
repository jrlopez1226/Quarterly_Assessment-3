import tkinter as tk
from tkinter import messagebox
import admin
import quiz_app as quiz

# Global root reference
main_app = None

# Launch functions with return capability
def launch_admin(root):
    admin.AdminApp(root, return_to_main=lambda: main_app.build_interface())

def launch_quiz(root):
    quiz.QuizApp(root, return_to_main=lambda: main_app.build_interface())

class EntryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to Quiz Application")
        self.root.geometry("400x300")
        self.build_interface()

    def build_interface(self):
        self.clear_screen()
        tk.Label(self.root, text="Select User Type", font=("Arial", 18)).pack(pady=20)

        tk.Button(self.root, text="Administrator", width=20, command=self.launch_admin_interface).pack(pady=10)
        tk.Button(self.root, text="Quiz Taker", width=20, command=self.launch_quiz_taker).pack(pady=10)

    def launch_admin_interface(self):
        self.clear_screen()
        launch_admin(self.root)

    def launch_quiz_taker(self):
        self.clear_screen()
        launch_quiz(self.root)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    main_app = EntryApp(root)
    root.mainloop()