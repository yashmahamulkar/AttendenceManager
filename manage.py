import tkinter as tk
from tkinter import ttk, simpledialog, messagebox,PhotoImage
import sqlite3 as sql


class AttendanceManager:
    
    def __init__(self, master):
        
        self.master = master
        self.master.title("MENU")
        width = 225
        height = 300
        screenwidth = self.master.winfo_screenwidth()
        screenheight = self.master.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.master.geometry(alignstr)
        self.master.resizable(width=False, height=False)

  
        self.conn = sql.connect("user_database.db")
        self.cur = self.conn.cursor()
        self.create_table()
       

        self.mainframe = ttk.Frame(self.master, padding="10")
        
        self.mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        
 
        self.create_widgets()



    def create_table(self):
        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS attable(subid INTEGER PRIMARY KEY, subject TEXT, attended INTEGER, bunked INTEGER, percentage NUMERIC,id int ,FOREIGN KEY (id) REFERENCES users (id))')
        self.conn.commit()

   


    def create_widgets(self):

      
        self.menu_label = ttk.Label(
        self.mainframe, text="Attendance Manager", font=("Arial", 16),)

        self.menu_label.grid(row=0, column=0, columnspan=1, pady=20)

        self.menu_buttons = [
            ("Add New Record", self.add_new_record),
            ("Manage Attendance", self.manage_attendance),
            ("Delete Record", self.delete_record),
            ("Edit Record", self.edit_record),
            ("Add Subjects", self.add_subjects),
      
            ("Exit", self.exit_app)
        ]

        for i, (text, command) in enumerate(self.menu_buttons):
            ttk.Button(self.mainframe, text=text, command=command).grid(
                row=i+1, column=0, pady=5, padx=10, sticky=tk.E+tk.W)

    def add_new_record(self):
        subjects = simpledialog.askstring(
            "Input", "Enter subject names separated by commas (e.g., Maths,Physics):")
        if subjects:
            self.cur.execute('DROP TABLE IF EXISTS attable')
            self.create_table()
            subjects = subjects.split(",")
            for sub in subjects:
                self.cur.execute(
                    'INSERT INTO attable (subject, attended, bunked, percentage) VALUES (?, ?, ?, ?)', (sub.strip(), 0, 0, 0))
            self.conn.commit()
            messagebox.showinfo("Success", "Subjects added successfully!")

    def manage_attendance(self):
        window = tk.Toplevel(self.master)
        window.title("Manage Attendance")

        self.cur.execute('SELECT * FROM attable')
        records = self.cur.fetchall()

        if records:
            for i, (subid, subject, attended, bunked,percentage,id) in enumerate(records):
                ttk.Label(window, text=f"Subject: {subject}, Attended: {attended}, Bunked: {bunked}, Percentage: {percentage}%").grid(
                    row=i, column=0, pady=5, padx=5)
        else:
            ttk.Label(window, text="No records found.").grid(row=0, column=0)

    def delete_record(self):
        self.cur.execute('DROP TABLE IF EXISTS attable')
        self.conn.commit()
        messagebox.showinfo("Success", "Records deleted!")

    def edit_record(self):
        sub_id = simpledialog.askinteger("Input", "Enter Subject ID:")
        if sub_id:
            self.cur.execute("SELECT * FROM attable WHERE subid=?", (sub_id,))
            record = self.cur.fetchone()

            if record:
                attended = simpledialog.askinteger(
                    "Input", f"Enter number of times attended for {record[1]}:")
                bunked = simpledialog.askinteger(
                    "Input", f"Enter number of times bunked for {record[1]}:")

                if attended is not None and bunked is not None:
                    new_attended = record[2] + attended
                    new_bunked = record[3] + bunked
                    percentage = new_attended/(new_attended + new_bunked)*100
                    self.cur.execute(
                        "UPDATE attable SET attended=?, bunked=?, percentage=? WHERE subid=?", (new_attended, new_bunked, percentage, sub_id))
                    self.conn.commit()
                    messagebox.showinfo("Success", "Record updated successfully!")
                else:
                    messagebox.showerror("Error", "Invalid input!")
            else:
                messagebox.showerror("Error", "Subject ID not found!")

    def add_subjects(self):
        subjects = simpledialog.askstring(
            "Input", "Enter subject names separated by commas (e.g., Math,Science):")
        if subjects:
            subjects = subjects.split(",")
            for sub in subjects:
                self.cur.execute(
                    'INSERT INTO attable (subject, attended, bunked) VALUES (?, ?, ?)', (sub.strip(), 0, 0))
            self.conn.commit()
            messagebox.showinfo("Success", "Subjects added successfully!")

    def exit_app(self):
        self.conn.close()
        self.master.destroy()
        


def main():
    root = tk.Tk()
  
    app = AttendanceManager(master=root)
    root.mainloop()



main()