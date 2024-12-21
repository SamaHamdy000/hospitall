import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def open_gui(file_name):
    try:
        os.system(f"python {file_name}")
    except Exception as e:
        messagebox.showerror("Error", f"Unable to open {file_name}: {str(e)}")

def exit_app():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()

def on_enter(button, hover_color):
    button.configure(bg=hover_color)

def on_leave(button, original_color):
    button.configure(bg=original_color)

root = tk.Tk()
root.title("Hospital Management System")
root.geometry("1200x1000")

background_image_path = "images/main_pg.jpg"
if os.path.exists(background_image_path):
    bg_image = Image.open(background_image_path).resize((1200, 1000), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
else:
    bg_photo = None

canvas = tk.Canvas(root, width=1500, height=1000, highlightthickness=0)
canvas.place(relwidth=1, relheight=1)

if bg_photo:
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

center_frame = tk.Frame(canvas, bd=0)
center_frame.place(relx=0.5, rely=0.5, anchor="center")

title_label = tk.Label(
    center_frame,
    text="Hospital Management System",
    font=("Arial", 24, "bold"),
    fg="#007BFF",
)
title_label.grid(row=0, column=0, columnspan=3, pady=(10, 20))

gui_files = [
    ("Doctor Management", "screens\doctor.py", "icons/doctor.png"),
    ("Hospital Management", "screens\hospital_management.py", "icons/hospital.png"),
    ("Lab Assistant Management", "screens\lab_assistant.py", "icons/lab_assistant.png"),
    ("Lab Test Management", "screens\lab_test.py", "icons/lab_test.png"),
    ("Medicine Management", "screens\medicine.py", "icons/medicine.png"),
    ("Nurse Management", "screens\screenNurse.py", "icons/nurse.png"),
    ("Patient Management", "screens\patient.py", "icons/patient.png"),
    ("PharmAssistant Management", "screens\pharmassistant.py", "icons/patient.png"),
    ("Receptionist Management", "screens\Receptionist.py", "icons/receptionist.png"),
    ("Staff Management", "screens\staff.py", "icons/staff.png"),
]

for index, (gui_name, gui_file, icon_path) in enumerate(gui_files):
    if os.path.exists(icon_path):
        icon_image = Image.open(icon_path).resize((50, 50), Image.Resampling.LANCZOS)
        icon = ImageTk.PhotoImage(icon_image)
    else:
        icon = None

    original_color = "#007BFF"
    hover_color = "#0056b3"

    button = tk.Button(
        center_frame,
        text=gui_name,
        image=icon,
        compound="top",
        command=lambda f=gui_file: open_gui(f),
        font=("Arial", 12),
        bg=original_color,
        fg="white",
        relief="groove",
        cursor="hand2",
        bd=1,
        padx=20,
        pady=10,
        width=150,
    )
    button.image = icon

    button.bind("<Enter>", lambda e, b=button, hc=hover_color: on_enter(b, hc))
    button.bind("<Leave>", lambda e, b=button, oc=original_color: on_leave(b, oc))

    row = (index // 3) + 1
    col = index % 3
    button.grid(row=row, column=col, padx=20, pady=10)

exit_button = tk.Button(
    center_frame,
    text="Exit",
    command=exit_app,
    font=("Arial", 14),
    bg="#FF5733",
    fg="white",
    cursor="hand2",
    width=20,
    relief="raised",
    bd=3,
)
exit_button.grid(
    row=(len(gui_files) // 3) + 2, column=0, columnspan=3, pady=(20, 10), sticky="s"
)

exit_button_original_color = "#FF5733"
exit_button_hover_color = "#cc4627"

exit_button.bind("<Enter>", lambda e: on_enter(exit_button, exit_button_hover_color))
exit_button.bind("<Leave>", lambda e: on_leave(exit_button, exit_button_original_color))

root.mainloop()