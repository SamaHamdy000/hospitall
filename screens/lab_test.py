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
            CREATE TABLE IF NOT EXISTS LabTest (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL
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

class LabTest:
    def __init__(self, db):
        self.db = db

    def create_lab_test(self, name, price):
        self.db.execute_query("INSERT INTO LabTest (name, price) VALUES (?, ?)", (name, price))

    def read_lab_test(self, lab_test_id):
        return self.db.fetch_query("SELECT * FROM LabTest WHERE id = ?", (lab_test_id,))

    def update_lab_test(self, lab_test_id, field, value):
        self.db.execute_query(f"UPDATE LabTest SET {field} = ? WHERE id = ?", (value, lab_test_id))

    def delete_lab_test(self, lab_test_id):
        self.db.execute_query("DELETE FROM LabTest WHERE id = ?", (lab_test_id,))

    def get_all_lab_tests(self):
        return self.db.fetch_query("SELECT * FROM LabTest")

class GUILabTest:
    def __init__(self, root, labTest):
        self.root = root
        self.labTest = labTest
        self.root.title("Lab Test Management")
        self.root.geometry("1500x1000")
        self.root.config(bg="#2C3E50")

        self.selected_lab_test_id = None

        self.create_input_fields()
        self.create_table()

    def create_input_fields(self):
        input_frame = tk.Frame(self.root, bg="#2C3E50")
        input_frame.pack(side="left")

        labels = ["Name", "Price"]
        self.entries = {}

        for idx, label in enumerate(labels):
            tk.Label(input_frame, text=label, foreground="white", bg="#2C3E50", font=("times", 12, "bold")).grid(row=idx, column=0, sticky="e")

            entry = tk.Entry(input_frame, width=30, font=("times", 12), relief="solid")
            entry.grid(row=idx, column=1, padx=5, pady=20)
            self.entries[label.lower().replace(" ", "_")] = entry

        self.add_button = tk.Button(input_frame, text="Add Test", command=self.add_lab_test, bg="#1ABC9C", bd=10,
                                    relief="flat", activebackground="#E0FAFF", activeforeground="white", foreground="white",
                                    font=("Helvetica", 12, "bold"), cursor="hand2", state="normal", pady=10)
        self.add_button.grid(row=len(labels), column=1, pady=10)

        self.delete_button = tk.Button(input_frame, text="Delete Test", command=self.delete_lab_test, bg="#E74C3C", bd=10,
                                        relief="flat", activebackground="#E0FAFF", activeforeground="white", foreground="white",
                                        font=("Helvetica", 12, "bold"), cursor="hand2", state="disabled", pady=10)
        self.delete_button.grid(row=len(labels) + 1, column=1, pady=10)

    def create_table(self):
        self.table = ttk.Treeview(self.root, columns=("ID", "Name", "Price"), show="headings", style="Treeview")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("times", 12, "bold"))

        for col in self.table["columns"]:
            self.table.heading(col, text=col)
            self.table.column(col, width=100, anchor="center")

        style.configure("Treeview", background="#CEF6FF", foreground="black", rowheight=25, fieldbackground="#CEF6FF")
        style.map("Treeview", background=[('selected', '#D1D8E0')])

        self.table.pack(fill=tk.BOTH, expand=True)
        self.load_lab_tests()

    def add_lab_test(self):
        try:
            data = {key: entry.get() for key, entry in self.entries.items()}
            self.labTest.create_lab_test(data["name"], float(data["price"]))
            messagebox.showinfo("Success", "Test added successfully.")
            self.load_lab_tests()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_lab_tests(self):
        for row in self.table.get_children():
            self.table.delete(row)

        for row in self.labTest.get_all_lab_tests():
            self.table.insert("", tk.END, values=row)

        self.table.bind("<ButtonRelease-1>", self.handle_row_select)

    def handle_row_select(self, event):
        item = self.table.identify('item', event.x, event.y)
        if item:
            values = self.table.item(item, "values")
            if values:
                self.selected_lab_test_id = values[0]
                self.entries["name"].delete(0, tk.END)
                self.entries["name"].insert(0, values[1])
                self.entries["price"].delete(0, tk.END)
                self.entries["price"].insert(0, values[2])
                self.delete_button.config(state="normal")

                self.add_button.config(
                    text="Update Test",
                    command=self.update_lab_test,
                    bg="#1ABC9C"
                )
            else:
                self.clear_selection()

    def clear_selection(self):
        self.selected_lab_test_id = None
        self.delete_button.config(state="disabled")
        self.add_button.config(
            text="Add Test",
            command=self.add_lab_test,
            bg="#1ABC9C"
        )
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def update_lab_test(self):
        if self.selected_lab_test_id:
            try:
                data = {key: entry.get() for key, entry in self.entries.items()}
                self.labTest.update_lab_test(
                    self.selected_lab_test_id,
                    "name",
                    data["name"]
                )
                self.labTest.update_lab_test(
                    self.selected_lab_test_id,
                    "price",
                    float(data["price"])
                )
                messagebox.showinfo("Success", "Test updated successfully.")
                self.clear_selection()
                self.load_lab_tests()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def delete_lab_test(self):
        if self.selected_lab_test_id:
            confirm = messagebox.askyesno("Confirm", f"Delete lab test with ID {self.selected_lab_test_id}?")
            if confirm:
                self.labTest.delete_lab_test(self.selected_lab_test_id)
                self.selected_lab_test_id = None
                self.delete_button.config(state="disabled")
                self.load_lab_tests()

if __name__ == "__main__":
    db = HospitalDB()
    labTest = LabTest(db)
    root = tk.Tk()
    gui = GUILabTest(root, labTest)
    root.mainloop()
    db.close()