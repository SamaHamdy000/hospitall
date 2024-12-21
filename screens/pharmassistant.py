import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DATABASE = "projectDatabase.db"

class HospitalDB:
    def __init__(self, db_name=DATABASE):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS PharmAssistant (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                gender TEXT DEFAULT 'Unknown',
                age INTEGER,
                bloodgroup TEXT,
                address TEXT,
                joined TEXT,
                certificates TEXT,
                education TEXT
            )
        """)
        self.conn.commit()

    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_query(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

class PharmAssistant:
    def __init__(self, db):
        self.db = db

    def create_pharm_assistant(self, name, phone, gender, age, bloodgroup, address, joined, certificates, education):
        self.db.execute_query(
            "INSERT INTO PharmAssistant (name, phone, gender, age, bloodgroup, address, joined, certificates, education) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (name, phone, gender, age, bloodgroup, address, joined, certificates, education)
        )

    def update_pharm_assistant(self, id, name, phone, gender, age, bloodgroup, address, joined, certificates, education):
        self.db.execute_query(
            "UPDATE PharmAssistant SET name=?, phone=?, gender=?, age=?, bloodgroup=?, address=?, joined=?, certificates=?, education=? WHERE id=?",
            (name, phone, gender, age, bloodgroup, address, joined, certificates, education, id)
        )

    def delete_pharm_assistant(self, id):
        self.db.execute_query("DELETE FROM PharmAssistant WHERE id = ?", (id,))

    def get_all_pharm_assistants(self):
        return self.db.fetch_query("SELECT * FROM PharmAssistant")

class GUIPharmacist:
    def __init__(self, root, pharm_assistant):
        self.root = root
        self.pharm_assistant = pharm_assistant
        self.root.title("Pharmacist Management")
        self.root.geometry("1500x1000")
        self.root.config(bg="#34495E")
        self.selected_id = None
        self.create_input_fields()
        self.create_table()

    def create_input_fields(self):
        input_frame = tk.Frame(self.root, bg="#2C3E50")
        input_frame.pack(side="left")

        labels = [
            "Name", "Phone", "Gender", "Age", "Blood Group", "Address", "Joined Date", "Certificates", "Education"
        ]
        self.entries = {}
        for idx, label in enumerate(labels):
            tk.Label(input_frame, text=label, bg="#2C3E50", fg="white", font=("times", 12, "bold")).grid(row=idx, column=0, sticky="e")
            if label == "Gender":
                entry = ttk.Combobox(input_frame, values=["Male", "Female"], state="readonly", width=38)
            elif label == "Blood Group":
                entry = ttk.Combobox(input_frame, values=["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"], state="readonly", width=38)
            else:
                entry = tk.Entry(input_frame, width=30, font=("times", 12), relief="solid")
            entry.grid(row=idx, column=1, padx=5, pady=20)
            self.entries[label.lower().replace(" ", "_")] = entry

        validate_age = (self.root.register(self.validate_age), '%P')
        self.entries["age"].config(validate="key", validatecommand=validate_age)

        self.add_button = tk.Button(input_frame, text="Add Pharmacist", command=self.add_or_update_pharmacist, bg="#1ABC9C", font=("Helvetica", 12, "bold"), fg="white", cursor="hand2")
        self.add_button.grid(row=len(labels), column=1, pady=10)
        self.add_button.bind("<Enter>", lambda e, b=self.add_button: self.on_button_hover_in(b, "#16A085"))
        self.add_button.bind("<Leave>", lambda e, b=self.add_button: self.on_button_hover_out(b, "#1ABC9C"))

        self.delete_button = tk.Button(input_frame, text="Delete Pharmacist", font=("Helvetica", 12, "bold"), bg="#E74C3C", fg="white", cursor="hand2", command=self.delete_selected_pharmacist)
        self.delete_button.grid(row=len(labels) + 1, column=1, pady=10)
        self.delete_button.bind("<Enter>", lambda e, b=self.delete_button: self.on_button_hover_in(b, "#C0392B"))
        self.delete_button.bind("<Leave>", lambda e, b=self.delete_button: self.on_button_hover_out(b, "#E74C3C"))

    def create_table(self):
        self.table = ttk.Treeview(self.root, columns=("ID", "Name", "Phone", "Gender", "Age", "Blood Group", "Address", "Joined Date", "Certificates", "Education"), show="headings", style="Treeview")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("times", 12, "bold"))

        for col in self.table["columns"]:
            self.table.heading(col, text=col)
            self.table.column(col, width=100, anchor="center")

        style.configure("Treeview", background="#CEF6FF", foreground="black", rowheight=25, fieldbackground="#CEF6FF")
        style.map("Treeview", background=[('selected', '#D1D8E0')])

        self.table.pack(fill=tk.BOTH, expand=True)
        self.load_pharmacists()

        self.table.bind("<ButtonRelease-1>", self.on_select)

    def on_button_hover_in(self, button, color):
        button.config(bg=color)

    def on_button_hover_out(self, button, color):
        button.config(bg=color)

    def validate_age(self, input_value):
        return input_value.isdigit() or input_value == ""

    def add_or_update_pharmacist(self):
        data = {key: entry.get() for key, entry in self.entries.items()}
        try:
            if self.selected_id is None:
                self.pharm_assistant.create_pharm_assistant(
                    data["name"], data["phone"], data["gender"], int(data["age"]),
                    data["blood_group"], data["address"], data["joined_date"],
                    data["certificates"], data["education"]
                )
                messagebox.showinfo("Success", "Pharmacist added successfully.")
            else:
                self.pharm_assistant.update_pharm_assistant(
                    self.selected_id, data["name"], data["phone"], data["gender"], int(data["age"]),
                    data["blood_group"], data["address"], data["joined_date"],
                    data["certificates"], data["education"]
                )
                messagebox.showinfo("Success", "Pharmacist updated successfully.")
            self.load_pharmacists()
            self.reset_form()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_selected_pharmacist(self):
        if self.selected_id:
            confirm = messagebox.askyesno("Confirm", f"Delete pharmacist with ID {self.selected_id}?")
            if confirm:
                self.pharm_assistant.delete_pharm_assistant(self.selected_id)
                self.load_pharmacists()
                self.reset_form()

    def load_pharmacists(self):
        for row in self.table.get_children():
            self.table.delete(row)

        for row in self.pharm_assistant.get_all_pharm_assistants():
            self.table.insert("", tk.END, values=row)

    def on_select(self, event):
        item = self.table.identify('item', event.x, event.y)
        values = self.table.item(item, "values")
        if values:
            self.selected_id = values[0]
            self.delete_button.config(state="normal")
            self.add_button.config(text="Update")

            self.entries["name"].delete(0, tk.END)
            self.entries["name"].insert(0, values[1])
            self.entries["phone"].delete(0, tk.END)
            self.entries["phone"].insert(0, values[2])
            self.entries["gender"].set(values[3])
            self.entries["age"].delete(0, tk.END)
            self.entries["age"].insert(0, values[4])
            self.entries["blood_group"].delete(0, tk.END)
            self.entries["blood_group"].insert(0, values[5])
            self.entries["address"].delete(0, tk.END)
            self.entries["address"].insert(0, values[6])
            self.entries["joined_date"].delete(0, tk.END)
            self.entries["joined_date"].insert(0, values[7])
            self.entries["certificates"].delete(0, tk.END)
            self.entries["certificates"].insert(0, values[8])
            self.entries["education"].delete(0, tk.END)
            self.entries["education"].insert(0, values[9])
        else:
            self.selected_id = None
            self.delete_button.config(state="disabled")

    def reset_form(self):
        self.selected_id = None
        self.add_button.config(text="Add Pharmacist")
        self.delete_button.config(state="disabled")
        for entry in self.entries.values():
            entry.delete(0, tk.END)

if __name__ == "__main__":
    db = HospitalDB()
    pharm_assistant = PharmAssistant(db)
    root = tk.Tk()
    gui = GUIPharmacist(root, pharm_assistant)
    root.mainloop()
    db.close()