import os
import re
import subprocess
from tkinter import PhotoImage, messagebox
from PIL import Image, ImageTk
import tkinter as tk
import sqlite3

class HospitalSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("900x500")
        # window icon 
        photo=PhotoImage(file="icons/hospital.png")
        root.iconphoto(True, photo) 
        root.resizable(False,False) 

        self.setup_background()
        self.setup_database()
        self.create_sign_up_gui()

    def setup_background(self):
        self.background_image = Image.open("images/hospital.jpg").resize((900, 500))
        self.bg_photo = ImageTk.PhotoImage(self.background_image)
        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def setup_database(self):
        self.conn = sqlite3.connect('projectDatabase.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL UNIQUE,
                                password TEXT NOT NULL)''')
        self.conn.commit()

    def create_sign_up_gui(self):
        self.clear_window()

        center_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
        center_frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=450)

        tk.Label(center_frame, text="Sign Up", fg="blue", font=("Arial", 20, "bold"), bg="white").pack(pady=10)

        tk.Label(center_frame, text="Username:", font=("Arial", 12), bg="white").pack(anchor="w", pady=5)
        self.username_entry = tk.Entry(center_frame, font=("Arial", 12), width=30)
        self.username_entry.pack(pady=5)

        tk.Label(center_frame, text="Password:", font=("Arial", 12), bg="white").pack(anchor="w", pady=5)
        self.password_entry = tk.Entry(center_frame, show='*', font=("Arial", 12), width=30)
        self.password_entry.pack(pady=5)

        tk.Label(center_frame, text="Confirm Password:", font=("Arial", 12), bg="white").pack(anchor="w", pady=5)
        self.confirm_password_entry = tk.Entry(center_frame, show='*', font=("Arial", 12), width=30)
        self.confirm_password_entry.pack(pady=5)

        register_button = tk.Button(center_frame, text="Register", command=self.register_user,
                                    font=("Arial", 12, "bold"), bg="blue", fg="white", cursor="hand2")
        register_button.pack(pady=20)
        self.add_hover_effect(register_button, "#1E90FF", "blue")

        sign_frame = tk.Frame(center_frame, bg="white")
        sign_frame.pack(pady=10)

        tk.Label(sign_frame, text="Already have an account? ", font=("Arial", 12), bg="white").pack(side="left", padx=5)
        sign_in_label = tk.Label(sign_frame, text="Sign In", fg="blue", font=("Arial", 12, "bold"), bg="white", cursor="hand2")
        sign_in_label.pack(side="left")
        sign_in_label.bind("<Button-1>", lambda e: self.create_sign_in_gui())

    def create_sign_in_gui(self):
        self.clear_window()

        center_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
        center_frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=350)

        tk.Label(center_frame, text="Sign In", fg="blue", font=("Arial", 20, "bold"), bg="white").pack(pady=10)

        tk.Label(center_frame, text="Username:", font=("Arial", 12), bg="white").pack(anchor="w", pady=5)
        self.sign_in_username_entry = tk.Entry(center_frame, font=("Arial", 12), width=30)
        self.sign_in_username_entry.pack(pady=5)

        tk.Label(center_frame, text="Password:", font=("Arial", 12), bg="white").pack(anchor="w", pady=5)
        self.sign_in_password_entry = tk.Entry(center_frame, show='*', font=("Arial", 12), width=30)
        self.sign_in_password_entry.pack(pady=5)

        sign_in_button = tk.Button(center_frame, text="Sign In", command=self.sign_in_user,
                                    font=("Arial", 12, "bold"), bg="blue", fg="white", cursor="hand2")
        sign_in_button.pack(pady=20)
        self.add_hover_effect(sign_in_button, "#1E90FF", "blue")

        sign_frame = tk.Frame(center_frame, bg="white")
        sign_frame.pack(pady=10)

        tk.Label(sign_frame, text="Don't have an account? ", font=("Arial", 12), bg="white").pack(side="left", padx=5)
        sign_up_label = tk.Label(sign_frame, text="Sign Up", fg="blue", font=("Arial", 12, "bold"), bg="white", cursor="hand2")
        sign_up_label.pack(side="left")
        sign_up_label.bind("<Button-1>", lambda e: self.create_sign_up_gui())
  

    def register_user(self):
     username = self.username_entry.get().strip()
     password = self.password_entry.get().strip()
     confirm_password = self.confirm_password_entry.get().strip()

     if not username or not password or not confirm_password:
        messagebox.showerror("Input Error", "Please fill out all fields.")
        return

     if password != confirm_password:
        messagebox.showerror("Password Error", "Passwords do not match.")
        return

    # password check
     if len(password) < 8:
        messagebox.showerror("Password Error", "Password must be at least 8 characters long and one special character (!@#$%^&* etc.)..")
        return

     if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  
        messagebox.showerror("Password Error", "Password must contain at least one special character (!@#$%^&* etc.).")
        return

     try:
        self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        self.conn.commit()
        messagebox.showinfo("Success", "User registered successfully!")
        self.create_sign_in_gui()
        self.clear_entries()
     except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")


    def sign_in_user(self):
        username = self.sign_in_username_entry.get().strip()
        password = self.sign_in_password_entry.get().strip()

        self.cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = self.cursor.fetchone()

        if user:
            messagebox.showinfo("Success", "Logged in successfully!")
            self.root.destroy()
            subprocess.Popen(["python", "home_page.py"])
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, image=self.bg_photo).place(x=0, y=0, relwidth=1, relheight=1)

    def clear_entries(self):
        if hasattr(self, 'username_entry'):
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)

    def add_hover_effect(self, widget, hover_color, default_color):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_color))
        widget.bind("<Leave>", lambda e: widget.config(bg=default_color))

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalSystemApp(root)
    root.mainloop()