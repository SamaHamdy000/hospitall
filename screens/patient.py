import tkinter
import tkinter.ttk
import tkinter.messagebox
import sqlite3

class Database:
    def __init__(self):
        self.dbConnection = sqlite3.connect("projectDatabase.db")
        self.dbCursor = self.dbConnection.cursor()
        self.dbCursor.execute("Create Table if not exists patient_info (id integer Primary Key, fName text, lName text, dob text, mob text, yob text, gender text, address text, phone text, email text, bloodGroup text, history text, doctor text)")

    def __del__(self):
        self.dbCursor.close()
        self.dbConnection.close()

    def Insert(self, id, fName, lName, dob, mob, yob, gender, address, phone, email, bloodGroup, history, doctor):
        self.dbCursor.execute("Insert into patient_info VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (id, fName, lName, dob, mob, yob, gender, address, phone, email, bloodGroup, history, doctor))
        self.dbConnection.commit()

    def Update(self, fName, lName, dob, mob, yob, gender, address, phone, email, bloodGroup, history, doctor, id):
        self.dbCursor.execute("UPDATE patient_info SET fName = ?, lName = ?, dob = ?, mob = ?, yob = ?, gender = ?, address = ?, phone = ?, email = ?, bloodGroup = ?, history = ?, doctor = ? WHERE id = ?", (fName, lName, dob, mob, yob, gender, address, phone, email, bloodGroup, history, doctor, id))
        self.dbConnection.commit()

    def Search(self, id):
        self.dbCursor.execute("SELECT * FROM patient_info WHERE id = ?", (id, ))
        searchResults = self.dbCursor.fetchall()
        return searchResults

    def Delete(self, id):
        self.dbCursor.execute("DELETE FROM patient_info WHERE id = ?", (id, ))
        self.dbConnection.commit()

    def Display(self):
        self.dbCursor.execute("SELECT * FROM patient_info")
        records = self.dbCursor.fetchall()
        return records

class Values:
    def Validate(self, id, fName, lName, phone, email, history, doctor):
        if not id or not id.isalnum():
            return "id"
        elif not (fName.isalpha()):
            return "fName"
        elif not (lName.isalpha()):
            return "lName"
        elif not (phone.isdigit() and (len(phone) == 11)):
            return "phone"
        elif not (email.count("@") == 1 and email.count(".") > 0):
            return "email"
        elif not (history.isalpha()):
            return "history"
        elif not (doctor.isalpha()):
            return "doctor"
        else:
            return "SUCCESS"

class InsertWindow:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.wm_title("Insert data")
        self.window.configure(bg="#2C3E50")
        self.window.resizable(False,False)

        self.id = tkinter.StringVar()
        self.fName = tkinter.StringVar()
        self.lName = tkinter.StringVar()
        self.address = tkinter.StringVar()
        self.phone = tkinter.StringVar()
        self.email = tkinter.StringVar()
        self.history = tkinter.StringVar()
        self.doctor = tkinter.StringVar()

        self.genderList = ["Male", "Female"]
        self.dateList = list(range(1, 32))
        self.monthList = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.yearList = list(range(1950, 2024))
        self.bloodGroupList = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

        tkinter.Label(self.window, text = "Patient ID", width = 25 , bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 1 )
        tkinter.Label(self.window, text = "First Name", width = 25 , bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 2)
        tkinter.Label(self.window, text = "Last Name", width = 25 , bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 3)
        tkinter.Label(self.window, text = "Day Of Birth", width = 25 , bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 4)
        tkinter.Label(self.window, text = "Month Of Birth", width = 25 , bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 5)
        tkinter.Label(self.window, text = "Year Of Birth", width = 25 , bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 6)
        tkinter.Label(self.window, text = "Gender", width = 25 , bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 7)
        tkinter.Label(self.window, text = "Home Address", width = 25 , bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 8)
        tkinter.Label(self.window, text = "Phone Number", width = 25 , bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 9)
        tkinter.Label(self.window, text = "Email", width = 25 , bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 10)
        tkinter.Label(self.window, text = "Blood Group", width = 25 , bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 11)
        tkinter.Label(self.window, text = "Patient History", width = 25 , bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 12)
        tkinter.Label(self.window, text = "Doctor", width = 25 , bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 13)


        self.idEntry = tkinter.Entry(self.window, width = 25, textvariable = self.id)
        self.fNameEntry = tkinter.Entry(self.window, width = 25, textvariable = self.fName)
        self.lNameEntry = tkinter.Entry(self.window, width = 25, textvariable = self.lName)
        self.addressEntry = tkinter.Entry(self.window, width = 25, textvariable = self.address)
        self.phoneEntry = tkinter.Entry(self.window, width = 25, textvariable = self.phone)
        self.emailEntry = tkinter.Entry(self.window, width = 25, textvariable = self.email)
        self.historyEntry = tkinter.Entry(self.window, width = 25, textvariable = self.history)
        self.doctorEntry = tkinter.Entry(self.window, width = 25, textvariable = self.doctor)

        self.idEntry.grid(pady = 5, column = 3, row = 1)
        self.fNameEntry.grid(pady = 5, column = 3, row = 2)
        self.lNameEntry.grid(pady = 5, column = 3, row = 3)
        self.addressEntry.grid(pady = 5, column = 3, row = 8)
        self.phoneEntry.grid(pady = 5, column = 3, row = 9)
        self.emailEntry.grid(pady = 5, column = 3, row = 10)
        self.historyEntry.grid(pady = 5, column = 3, row = 12)
        self.doctorEntry.grid(pady = 5, column = 3, row = 13)

        self.dobBox = tkinter.ttk.Combobox(self.window, values = self.dateList, width = 22)
        self.mobBox = tkinter.ttk.Combobox(self.window, values = self.monthList, width = 22)
        self.yobBox = tkinter.ttk.Combobox(self.window, values = self.yearList, width = 22)
        self.genderBox = tkinter.ttk.Combobox(self.window, values = self.genderList, width = 22)
        self.bloodGroupBox = tkinter.ttk.Combobox(self.window, values = self.bloodGroupList, width = 22)

        self.dobBox.grid(pady = 5, column = 3, row = 4)
        self.mobBox.grid(pady = 5, column = 3, row = 5)
        self.yobBox.grid(pady = 5, column = 3, row = 6)
        self.genderBox.grid(pady = 5, column = 3, row = 7)
        self.bloodGroupBox.grid(pady = 5, column = 3, row = 11)

        tkinter.Button(self.window, width = 20, text = "Insert", command = self.Insert , bg="#1C3F50" , fg="white").grid(pady = 15, padx = 5, column = 1, row = 14)
        tkinter.Button(self.window, width = 20, text = "Reset", command = self.Reset, bg="light blue" , fg="black").grid(pady = 15, padx = 5, column = 2, row = 14)
        tkinter.Button(self.window, width = 20, text = "Close", command = self.window.destroy, bg="red" , fg="white").grid(pady = 15, padx = 5, column = 3, row = 14)

        self.window.mainloop()

    def Insert(self):
        self.values = Values()
        self.database = Database()
        self.test = self.values.Validate(self.idEntry.get(), self.fNameEntry.get(), self.lNameEntry.get(), self.phoneEntry.get(), self.emailEntry.get(), self.historyEntry.get(), self.doctorEntry.get())
        if (self.test == "SUCCESS"):
            self.database.Insert(self.idEntry.get(), self.fNameEntry.get(), self.lNameEntry.get(), self.dobBox.get(), self.mobBox.get(), self.yobBox.get(), self.genderBox.get(), self.addressEntry.get(), self.phoneEntry.get(), self.emailEntry.get(), self.bloodGroupBox.get(), self.historyEntry.get(), self.doctorEntry.get())
            tkinter.messagebox.showinfo("Inserted data", "Successfully inserted the above data in the database")
        else:
            self.valueErrorMessage = "Invalid input in field " + self.test
            tkinter.messagebox.showerror("Value Error", self.valueErrorMessage)

    def Reset(self):
        self.idEntry.delete(0, tkinter.END)
        self.fNameEntry.delete(0, tkinter.END)
        self.lNameEntry.delete(0, tkinter.END)
        self.dobBox.set("")
        self.mobBox.set("")
        self.yobBox.set("")
        self.genderBox.set("")
        self.addressEntry.delete(0, tkinter.END)
        self.phoneEntry.delete(0, tkinter.END)
        self.emailEntry.delete(0, tkinter.END)
        self.bloodGroupBox.set("")
        self.historyEntry.delete(0, tkinter.END)
        self.doctorEntry.delete(0, tkinter.END)
class UpdateWindow:
    def __init__(self, id):
        self.window = tkinter.Tk()
        self.window.wm_title("Update data")
        self.window.configure(bg="#2C3E50")
        self.window.resizable(False,False)

        self.id = id

        self.fName = tkinter.StringVar()
        self.lName = tkinter.StringVar()
        self.address = tkinter.StringVar()
        self.phone = tkinter.StringVar()
        self.email = tkinter.StringVar()
        self.history = tkinter.StringVar()
        self.doctor = tkinter.StringVar()

        self.genderList = ["Male", "Female"]
        self.dateList = list(range(1, 32))
        self.monthList = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.yearList = list(range(1950, 2024))
        self.bloodGroupList = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

        tkinter.Label(self.window, text = "Patient ID", width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 1)
        tkinter.Label(self.window, text = id, width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 2, row = 1)
        tkinter.Label(self.window, text = "First Name", width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 2)
        tkinter.Label(self.window, text = "Last Name", width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 3)
        tkinter.Label(self.window, text = "Day Of Birth", width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 4)
        tkinter.Label(self.window, text = "Month Of Birth", width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 5)
        tkinter.Label(self.window, text = "Year Of Birth", width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 6)
        tkinter.Label(self.window, text = "Gender", width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 7)
        tkinter.Label(self.window, text = "Home Address", width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 8)
        tkinter.Label(self.window, text = "Phone Number", width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 9)
        tkinter.Label(self.window, text = "Email", width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 10)
        tkinter.Label(self.window, text = "Blood Group", width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 11)
        tkinter.Label(self.window, text = "Patient History", width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 12)
        tkinter.Label(self.window, text = "Doctor", width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 1, row = 13)

        self.database = Database()
        self.searchResults = self.database.Search(id)

        tkinter.Label(self.window, text = self.searchResults[0][1], width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 2, row = 2)
        tkinter.Label(self.window, text = self.searchResults[0][1], width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 2, row = 2)
        tkinter.Label(self.window, text = self.searchResults[0][1], width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 2, row = 2)
        tkinter.Label(self.window, text = self.searchResults[0][2], width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 2, row = 3)
        tkinter.Label(self.window, text = self.searchResults[0][3], width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 2, row = 4)
        tkinter.Label(self.window, text = self.searchResults[0][4], width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 2, row = 5)
        tkinter.Label(self.window, text = self.searchResults[0][5], width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 2, row = 6)
        tkinter.Label(self.window, text = self.searchResults[0][6], width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 2, row = 7)
        tkinter.Label(self.window, text = self.searchResults[0][7], width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 2, row = 8)
        tkinter.Label(self.window, text = self.searchResults[0][8], width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 2, row = 9)
        tkinter.Label(self.window, text = self.searchResults[0][9], width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 2, row = 10)
        tkinter.Label(self.window, text = self.searchResults[0][10], width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 2, row = 11)
        tkinter.Label(self.window, text = self.searchResults[0][11], width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 2, row = 12)
        tkinter.Label(self.window, text = self.searchResults[0][12], width = 25, bg="#2C3E50" , fg="white" , font=("Helvetica", 10 , "bold")).grid(pady = 5, column = 2, row = 13)

        self.fNameEntry = tkinter.Entry(self.window, width = 25, textvariable = self.fName)
        self.lNameEntry = tkinter.Entry(self.window, width = 25, textvariable = self.lName)
        self.addressEntry = tkinter.Entry(self.window, width = 25, textvariable = self.address)
        self.phoneEntry = tkinter.Entry(self.window, width = 25, textvariable = self.phone)
        self.emailEntry = tkinter.Entry(self.window, width = 25, textvariable = self.email)
        self.historyEntry = tkinter.Entry(self.window, width = 25, textvariable = self.history)
        self.doctorEntry = tkinter.Entry(self.window, width = 25, textvariable = self.doctor)

        self.fNameEntry.grid(pady = 5, column = 3, row = 2)
        self.lNameEntry.grid(pady = 5, column = 3, row = 3)
        self.addressEntry.grid(pady = 5, column = 3, row = 8)
        self.phoneEntry.grid(pady = 5, column = 3, row = 9)
        self.emailEntry.grid(pady = 5, column = 3, row = 10)
        self.historyEntry.grid(pady = 5, column = 3, row = 12)
        self.doctorEntry.grid(pady = 5, column = 3, row = 13)

        self.dobBox = tkinter.ttk.Combobox(self.window, values = self.dateList, width = 22)
        self.mobBox = tkinter.ttk.Combobox(self.window, values = self.monthList, width = 22)
        self.yobBox = tkinter.ttk.Combobox(self.window, values = self.yearList, width = 22)
        self.genderBox = tkinter.ttk.Combobox(self.window, values = self.genderList, width = 22)
        self.bloodGroupBox = tkinter.ttk.Combobox(self.window, values = self.bloodGroupList, width = 22)

        self.dobBox.grid(pady = 5, column = 3, row = 4)
        self.mobBox.grid(pady = 5, column = 3, row = 5)
        self.yobBox.grid(pady = 5, column = 3, row = 6)
        self.genderBox.grid(pady = 5, column = 3, row = 7)
        self.bloodGroupBox.grid(pady = 5, column = 3, row = 11)

        tkinter.Button(self.window, width = 20, text = "Update", command = self.Update, bg="#1C3F50" , fg="white").grid(pady = 15, padx = 5, column = 1, row = 14)
        tkinter.Button(self.window, width = 20, text = "Reset", command = self.Reset, bg="light blue" , fg="black").grid(pady = 15, padx = 5, column = 2, row = 14)
        tkinter.Button(self.window, width = 20, text = "Close", command = self.window.destroy, bg="red" , fg="white").grid(pady = 15, padx = 5, column = 3, row = 14)

        self.window.mainloop()

    def Update(self):
        self.database = Database()
        self.database.Update(self.fNameEntry.get(), self.lNameEntry.get(), self.dobBox.get(), self.mobBox.get(), self.yobBox.get(), self.genderBox.get(), self.addressEntry.get(), self.phoneEntry.get(), self.emailEntry.get(), self.bloodGroupBox.get(), self.historyEntry.get(), self.doctorEntry.get(), self.id)
        tkinter.messagebox.showinfo("Updated data", "Successfully updated the above data in the database")

    def Reset(self):
        self.fNameEntry.delete(0, tkinter.END)
        self.lNameEntry.delete(0, tkinter.END)
        self.dobBox.set("")
        self.mobBox.set("")
        self.yobBox.set("")
        self.genderBox.set("")
        self.addressEntry.delete(0, tkinter.END)
        self.phoneEntry.delete(0, tkinter.END)
        self.emailEntry.delete(0, tkinter.END)
        self.bloodGroupBox.set("")
        self.historyEntry.delete(0, tkinter.END)
        self.doctorEntry.delete(0, tkinter.END)

class DatabaseView:
    def __init__(self, data):
        self.databaseViewWindow = tkinter.Tk()
        self.databaseViewWindow.wm_title("Database View")

        tkinter.Label(self.databaseViewWindow, text = "Database View Window", width = 25).grid(pady = 5, column = 1, row = 1)

        self.databaseView = tkinter.ttk.Treeview(self.databaseViewWindow)
        self.databaseView.grid(pady = 5, column = 1, row = 2)
        self.databaseView["show"] = "headings"
        self.databaseView["columns"] = ("id", "fName", "lName", "dob", "mob", "yob", "gender", "address", "phone", "email", "bloodGroup", "history", "doctor")

        self.databaseView.heading("id", text = "ID")
        self.databaseView.heading("fName", text = "First Name")
        self.databaseView.heading("lName", text = "Last Name")
        self.databaseView.heading("dob", text = "D.O.B")
        self.databaseView.heading("mob", text = "M.O.B")
        self.databaseView.heading("yob", text = "Y.O.B")
        self.databaseView.heading("gender", text = "Gender")
        self.databaseView.heading("address", text = "Home Address")
        self.databaseView.heading("phone", text = "Phone Number")
        self.databaseView.heading("email", text = "Email")
        self.databaseView.heading("bloodGroup", text = "Blood Group")
        self.databaseView.heading("history", text = "History")
        self.databaseView.heading("doctor", text = "Doctor")

        self.databaseView.column("id", width = 40)
        self.databaseView.column("fName", width = 100)
        self.databaseView.column("lName", width = 100)
        self.databaseView.column("dob", width = 60)
        self.databaseView.column("mob", width = 60)
        self.databaseView.column("yob", width = 60)
        self.databaseView.column("gender", width = 60)
        self.databaseView.column("address", width = 200)
        self.databaseView.column("phone", width = 100)
        self.databaseView.column("email", width = 200)
        self.databaseView.column("bloodGroup", width = 100)
        self.databaseView.column("history", width = 100)
        self.databaseView.column("doctor", width = 100)

        for record in data:
            self.databaseView.insert('', 'end', values=(record))

        self.databaseViewWindow.mainloop()

class SearchDeleteWindow:
    def __init__(self, task):
        window = tkinter.Tk()
        window.wm_title(task + " data")
        window.configure(bg="#2C3E50")
        window.resizable(False,False)

        self.id = tkinter.StringVar()
        self.fName = tkinter.StringVar()
        self.lName = tkinter.StringVar()
        self.heading = "Please enter Patient ID to " + task

        tkinter.Label(window, text = self.heading, width = 50 , bg="#2C3E50", fg = "white").grid(pady = 20, row = 1)
        tkinter.Label(window, text = "Patient ID", width = 10 , bg="#2C3E50", fg = "white").grid(pady = 5, row = 2)

        self.idEntry = tkinter.Entry(window, width = 5, textvariable = self.id)

        self.idEntry.grid(pady = 5, row = 3)

        if (task == "Search"):
            tkinter.Button(window, width = 20, text = task,bg="#1ABC9C",fg="white" , command = self.Search).grid(pady = 15, padx = 5, column = 0, row = 14)
        elif (task == "Delete"):
            tkinter.Button(window, width = 20, text = task,bg="#1ABC9C",fg="white" , command = self.Delete).grid(pady = 15, padx = 5, column = 0, row = 14)

    def Search(self):
        self.database = Database()
        self.data = self.database.Search(self.idEntry.get())
        if not self.data:
            tkinter.messagebox.showwarning("Not Found", "The ID you entered was not found.")
        else:
            self.databaseView = DatabaseView(self.data)

    def Delete(self):
        record_id = self.idEntry.get()
        self.database = Database()
        if not record_id:
                tkinter.messagebox.showwarning("Invalid Input", "Please enter a valid ID.")
                return
        success = self.database.Delete(record_id)
        if success:
            tkinter.messagebox.showinfo("Success", "The record was successfully deleted.")
        else:
            tkinter.messagebox.showwarning("Deletion Failed", "The ID you entered was not found or couldn't be deleted.")

class HomePage:
    def __init__(self):
        self.homePageWindow = tkinter.Tk()
        self.homePageWindow.wm_title("Patient Information System")
        self.homePageWindow.configure(bg="#2C3E50")
        self.homePageWindow.resizable(False,False)
        tkinter.Label(self.homePageWindow, text = "Patient Information System", font=("times",14,"bold","italic"), width = 100).grid(pady = 20, column = 1, row = 1)

        tkinter.Button(self.homePageWindow, width = 20, text = "Insert", relief="flat",bg="#1ABC9C",fg="white",font=("times",12),cursor="hand2",state="normal", command = self.Insert).grid(pady = 15, column = 1, row = 2)
        tkinter.Button(self.homePageWindow, width = 20, text = "Update", relief="flat",bg="#1ABC9C",fg="white",font=("times",12),cursor="hand2",state="normal", command = self.Update).grid(pady = 15, column = 1, row = 3)
        tkinter.Button(self.homePageWindow, width = 20, text = "Search", relief="flat",bg="#1ABC9C",fg="white",font=("times",12),cursor="hand2",state="normal", command = self.Search).grid(pady = 15, column = 1, row = 4)
        tkinter.Button(self.homePageWindow, width = 20, text = "Delete", relief="flat",bg="#1ABC9C",fg="white",font=("times",12),cursor="hand2",state="normal", command = self.Delete).grid(pady = 15, column = 1, row = 5)
        tkinter.Button(self.homePageWindow, width = 20, text = "Display", relief="flat",bg="#1ABC9C",fg="white",font=("times",12),cursor="hand2",state="normal", command = self.Display).grid(pady = 15, column = 1, row = 6)
        tkinter.Button(self.homePageWindow, width = 20, text = "Exit", relief="flat",bg="red",fg="white",font=("times",14,"underline"),cursor="hand2",state="normal", command = self.homePageWindow.destroy).grid(pady = 15, column = 1, row = 7)

        self.homePageWindow.mainloop()

    def Insert(self):
        self.insertWindow = InsertWindow()

    def Update(self):
        self.updateIDWindow = tkinter.Tk()
        self.updateIDWindow.wm_title("Update data")
        self.updateIDWindow.resizable(False,False)
        self.updateIDWindow.configure(bg="#2C3E50")

        self.id = tkinter.StringVar()

        tkinter.Label(self.updateIDWindow, text = "Enter the ID to update", width = 50 , bg="#2C3E50",fg="white").grid(pady = 20, row = 1)

        self.idEntry = tkinter.Entry(self.updateIDWindow, width = 5, textvariable = self.id)

        self.idEntry.grid(pady = 10, row = 2)

        tkinter.Button(self.updateIDWindow, width = 20,bg="#1ABC9C",fg="white" , text = "Update", command = self.updateID).grid(pady = 10, row = 3)

        self.updateIDWindow.mainloop()

    def updateID(self):
        self.updateWindow = UpdateWindow(self.idEntry.get())
        self.updateIDWindow.destroy()

    def Search(self):
        self.searchWindow = SearchDeleteWindow("Search")

    def Delete(self):
        self.deleteWindow = SearchDeleteWindow("Delete")

    def Display(self):
        self.database = Database()
        self.data = self.database.Display()
        self.displayWindow = DatabaseView(self.data)
        self.displayWindow.configure(bg="#2C3E50")

homePage = HomePage()