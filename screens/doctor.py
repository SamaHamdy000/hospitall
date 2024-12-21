import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

class DoctorManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Doctor Management System")
        self.root.geometry("1500x1000")
        self.root.configure(bg="#34495E")

        self.conn = sqlite3.connect("projectDatabase.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        self.init_variables()

        self.create_form_frame()
        self.create_table_frame()

        self.fetch_data()

        self.age_var.trace("w", self.validate_age)

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            gender TEXT,
            age INTEGER,
            blood_group TEXT,
            address TEXT,
            joined TEXT,
            certificates TEXT,
            education TEXT,
            specialty TEXT
        )
        """)
        self.conn.commit()

    def init_variables(self):
        self.selected_id = None
        self.name_var = StringVar()
        self.phone_var = StringVar()
        self.gender_var = StringVar()
        self.age_var = StringVar()
        self.blood_group_var = StringVar()
        self.address_var = StringVar()
        self.joined_var = StringVar()
        self.certificates_var = StringVar()
        self.education_var = StringVar()
        self.specialty_var = StringVar()

    def create_form_frame(self):
        form_frame = Frame(self.root, bg="#2C3E50", width=350)
        form_frame.pack(side=LEFT, fill=Y)

        fields = [
            ("Name", self.name_var),
            ("Phone", self.phone_var),
            ("Gender", self.gender_var),
            ("Age", self.age_var),
            ("Blood Group", self.blood_group_var),
            ("Address", self.address_var),
            ("Joined", self.joined_var),
            ("Certificates", self.certificates_var),
            ("Education", self.education_var),
            ("Specialty", self.specialty_var),
        ]

        for i, (label, var) in enumerate(fields):
            Label(form_frame, text=label, bg="#2C3E50", fg="white", font=("Helvetica", 12)).grid(row=i, column=0, padx=10, pady=5, sticky=W)
            if label == "Gender":
                widget = ttk.Combobox(form_frame, textvariable=var, state="readonly", width=23, font=("Helvetica", 12))
                widget["values"] = ("Male", "Female")
            elif label == "Blood Group":
                widget = ttk.Combobox(form_frame, textvariable=var, state="readonly", width=23, font=("Helvetica", 12))
                widget["values"] = ("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-")
            else:
                widget = Entry(form_frame, textvariable=var, width=25, font=("Helvetica", 12))
            widget.grid(row=i, column=1, padx=10, pady=5)

        self.action_button = Button(
            form_frame, text="Add Doctor", command=self.add_or_update_doctor,
            bg="#1ABC9C", fg="white", font=("Helvetica", 12, "bold"), cursor="hand2"
        )
        self.action_button.grid(row=len(fields), columnspan=2, pady=10)
        self.add_hover_effect(self.action_button, "#16A085", "#1ABC9C")

        self.delete_button = Button(
            form_frame, text="Delete Doctor", command=self.delete_doctor,
            bg="#E74C3C", fg="white", font=("Helvetica", 12, "bold"), cursor="hand2", state=DISABLED
        )
        self.delete_button.grid(row=len(fields) + 1, columnspan=2, pady=10)
        self.add_hover_effect(self.delete_button, "#C0392B", "#E74C3C")

    def add_hover_effect(self, button, hover_color, default_color):
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=default_color))

    def create_table_frame(self):
        table_frame = Frame(self.root, bg="#ECF0F1", width=500)
        table_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background="#3498DB", foreground="black")
        style.configure("Treeview", background="#ECF0F1", foreground="black", rowheight=25)

        self.doctor_table = ttk.Treeview(
            table_frame,
            columns=("ID", "Name", "Phone", "Gender", "Age", "Blood Group", "Address", "Joined", "Certificates", "Education", "Specialty"),
            show="headings"
        )
        self.doctor_table.pack(fill=BOTH, expand=True)

        for col in self.doctor_table["columns"]:
            self.doctor_table.heading(col, text=col)
            self.doctor_table.column(col, anchor=CENTER, stretch=True, width=100)

        self.doctor_table.bind("<ButtonRelease-1>", self.load_selected_row)

    def add_or_update_doctor(self):
        if self.selected_id:
            self.update_doctor()
        else:
            self.add_doctor()

    def add_doctor(self):
        if not self.all_fields_filled():
            messagebox.showerror("Error", "All fields must be filled.")
            return

        try:
            self.cursor.execute("""
            INSERT INTO doctor (name, phone, gender, age, blood_group, address, joined, certificates, education, specialty)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, self.get_field_values())
            self.conn.commit()
            messagebox.showinfo("Success", "Doctor added successfully.")
            self.clear_fields()
            self.fetch_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add doctor: {e}")

    def update_doctor(self):
        if not self.all_fields_filled():
            messagebox.showerror("Error", "All fields must be filled.")
            return

        try:
            self.cursor.execute("""
            UPDATE doctor SET name=?, phone=?, gender=?, age=?, blood_group=?, address=?, joined=?, certificates=?, education=?, specialty=?
            WHERE id=?
            """, (*self.get_field_values(), self.selected_id))
            self.conn.commit()
            messagebox.showinfo("Success", "Doctor updated successfully.")
            self.clear_fields()
            self.fetch_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update doctor: {e}")

    def delete_doctor(self):
        if not self.selected_id:
            messagebox.showerror("Error", "No doctor selected.")
            return

        self.cursor.execute("DELETE FROM doctor WHERE id=?", (self.selected_id,))
        self.conn.commit()
        messagebox.showinfo("Deleted", "Doctor deleted successfully.")
        self.clear_fields()
        self.fetch_data()

    def fetch_data(self):
        self.doctor_table.delete(*self.doctor_table.get_children())
        self.cursor.execute("SELECT * FROM doctor")
        for row in self.cursor.fetchall():
            self.doctor_table.insert("", END, values=row)

    def load_selected_row(self, event):
        selected = self.doctor_table.focus()
        if selected:
            values = self.doctor_table.item(selected, "values")
            if values:
                self.selected_id = values[0]
                fields = [
                    self.name_var, self.phone_var, self.gender_var, self.age_var,
                    self.blood_group_var, self.address_var, self.joined_var,
                    self.certificates_var, self.education_var, self.specialty_var
                ]
                for var, value in zip(fields, values[1:]):
                    var.set(value)
                self.action_button.config(text="Update")
                self.delete_button.config(state=NORMAL)

    def validate_age(self, *args):
        if self.age_var.get() and not self.age_var.get().isdigit():
            messagebox.showwarning("Input Error", "Age must be a number.")
            self.age_var.set("")

    def clear_fields(self):
        for var in [self.name_var, self.phone_var, self.gender_var, self.age_var,
                    self.blood_group_var, self.address_var, self.joined_var,
                    self.certificates_var, self.education_var, self.specialty_var]:
            var.set("")
        self.selected_id = None
        self.action_button.config(text="Add Doctor")
        self.delete_button.config(state=DISABLED)

    def all_fields_filled(self):
        return all(var.get() for var in [
            self.name_var, self.phone_var, self.gender_var, self.age_var,
            self.blood_group_var, self.address_var, self.joined_var,
            self.certificates_var, self.education_var, self.specialty_var
        ])

    def get_field_values(self):
        return (
            self.name_var.get(), self.phone_var.get(), self.gender_var.get(),
            self.age_var.get(), self.blood_group_var.get(), self.address_var.get(),
            self.joined_var.get(), self.certificates_var.get(),
            self.education_var.get(), self.specialty_var.get()
        )

if __name__ == "__main__":
    root = Tk()
    app = DoctorManagementApp(root)
    root.mainloop()