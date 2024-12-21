import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DATABASE = "projectDatabase.db"

class HospitalDB:
    def __init__(self, db_name=DATABASE):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS LabAssistant (
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
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

    def fetch_query(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return []

    def close(self):
        self.conn.close()

class LabAssistantManager:
    def __init__(self, db):
        self.db = db

    def create_LabAssistant(self, name, phone, gender, age, bloodgroup, address, joined, certificates, education):
        self.db.execute_query(
            "INSERT INTO LabAssistant (name, phone, gender, age, bloodgroup, address, joined, certificates, education) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (name, phone, gender, age, bloodgroup, address, joined, certificates, education)
        )

    def read_LabAssistant(self):
        return self.db.fetch_query("SELECT * FROM LabAssistant")

    def update_LabAssistant(self, id, name, phone, gender, age, bloodgroup, address, joined, certificates, education):
        self.db.execute_query(
            """UPDATE LabAssistant SET name = ?, phone = ?, gender = ?, age = ?, bloodgroup = ?, address = ?, joined = ?, certificates = ?, education = ? WHERE id = ?""",
            (name, phone, gender, age, bloodgroup, address, joined, certificates, education, id)
        )

    def delete_LabAssistant(self, id):
        self.db.execute_query("DELETE FROM LabAssistant WHERE id = ?", (id,))

class GUILabAssistant:
    def __init__(self, root, lab_assistant_manager):
        self.root = root
        self.lab_assistant_manager = lab_assistant_manager
        self.root.title("Lab Assistant Management")
        self.root.geometry("1500x1000")
        self.root.config(bg="#34495E")

        self.create_input_fields()
        self.create_table()
        self.selected_id = None

    def create_input_fields(self):
        input_frame = tk.Frame(self.root, bg="#2C3E50")
        input_frame.pack(side="left")

        labels = [
            "Name", "Phone", "Gender", "Age", "Blood Group", "Address", "Joined Date", "Certificates", "Education"
        ]
        self.entries = {}

        validate_age = (self.root.register(self.is_valid_age), "%P")

        for idx, label in enumerate(labels):
            tk.Label(input_frame, text=label, bg="#2C3E50", fg="white", font=("times", 12, "bold")).grid(row=idx, column=0, sticky="e")
            if label == "Gender":
                entry = ttk.Combobox(input_frame, values=["Male", "Female"], state="readonly", width=23)
            elif label == "Blood Group":
                entry = ttk.Combobox(input_frame, values=["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"], state="readonly", width=23)
            elif label == "Age":
                entry = tk.Entry(input_frame, width=20, font=("times", 12), relief="solid", validate="key", validatecommand=validate_age)
            else:
                entry = tk.Entry(input_frame, width=20, font=("times", 12), relief="solid")
            entry.grid(row=idx, column=1, padx=5, pady=20)
            self.entries[label.lower().replace(" ", "_")] = entry

        self.add_button = tk.Button(input_frame, text="Add Lab Assistant", command=self.add_or_update_lab_assistant, bg="#1ABC9C", bd=5, relief="flat", activebackground="#E0FAFF", fg="white", font=("times", 10, "bold"), cursor="hand2", pady=5, padx=5)
        self.add_button.grid(row=len(labels), column=1, pady=10)

        self.delete_button = tk.Button(input_frame, text="Delete Lab Assistant", command=self.delete_selected_lab_assistant, bg="#E74C3C", bd=5, relief="flat", activebackground="#F5B7B1", fg="white", font=("times", 10, "bold"), cursor="hand2", pady=5, padx=5, state="disabled")
        self.delete_button.grid(row=len(labels) + 1, column=1, pady=10)

    def is_valid_age(self, value):
        if value == "" or value.isdigit():
            return True
        return False

    def create_table(self):
        self.table = ttk.Treeview(self.root, columns=(
            "ID", "Name", "Phone", "Gender", "Age", "Blood Group", "Address", "Joined Date", "Certificates", "Education"
        ), show="headings", style="Treeview")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("times", 12, "bold"))

        for col in self.table["columns"]:
            self.table.heading(col, text=col)
            self.table.column(col, width=100, anchor="center")

        style = ttk.Style()
        style.configure("Treeview", background="#CEF6FF", foreground="black", rowheight=25, fieldbackground="#CEF6FF")
        style.map("Treeview", background=[('selected', '#D1D8E0')])

        self.table.pack(fill=tk.BOTH, expand=True)
        self.load_lab_assistants()

    def add_or_update_lab_assistant(self):
        try:
            for key, entry in self.entries.items():
                if isinstance(entry, ttk.Combobox):
                    value = entry.get()
                else:
                    value = entry.get().strip()
                if not value:
                    raise ValueError(f"Please fill in the {key.replace('_', ' ').title()} field.")

            data = {key: entry.get().strip() for key, entry in self.entries.items()}
            age = data["age"]

            if not age.isdigit() or not (18 <= int(age) <= 100):
                raise ValueError("Please enter a valid age between 18 and 100.")

            if self.selected_id:
                self.lab_assistant_manager.update_LabAssistant(
                    self.selected_id, data["name"], data["phone"], data["gender"], int(age),
                    data["blood_group"], data["address"], data["joined_date"], data["certificates"], data["education"]
                )
                messagebox.showinfo("Success", "Lab Assistant updated successfully.")
            else:
                self.lab_assistant_manager.create_LabAssistant(
                    data["name"], data["phone"], data["gender"], int(age),
                    data["blood_group"], data["address"], data["joined_date"],
                    data["certificates"], data["education"]
                )
                messagebox.showinfo("Success", "Lab Assistant added successfully.")

            self.load_lab_assistants()
            self.reset_form()
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_selected_lab_assistant(self):
        if self.selected_id:
            confirm = messagebox.askyesno("Confirm", f"Delete lab assistant with ID {self.selected_id}?")
            if confirm:
                self.lab_assistant_manager.delete_LabAssistant(self.selected_id)
                self.load_lab_assistants()
                self.reset_form()
        else:
            messagebox.showwarning("No selection", "Please select a lab assistant to delete.")

    def load_lab_assistants(self):
        for row in self.table.get_children():
            self.table.delete(row)

        for row in self.lab_assistant_manager.read_LabAssistant():
            self.table.insert("", tk.END, values=row)

        self.table.bind("<ButtonRelease-1>", self.handle_table_click)

    def handle_table_click(self, event):
        item = self.table.identify('item', event.x, event.y)
        values = self.table.item(item, "values")
        if values:
            self.selected_id = values[0]
            self.populate_form(values)

    def populate_form(self, values):
        for idx, key in enumerate(self.entries.keys()):
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, values[idx + 1])

        self.add_button.config(text="Update Lab Assistant")
        self.delete_button.config(state="normal")

    def reset_form(self):
        self.selected_id = None
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.add_button.config(text="Add Lab Assistant")
        self.delete_button.config(state="disabled")

if __name__ == "__main__":
    db = HospitalDB()
    lab_assistant_manager = LabAssistantManager(db)
    root = tk.Tk()
    gui = GUILabAssistant(root, lab_assistant_manager)
    root.mainloop()
    db.close()