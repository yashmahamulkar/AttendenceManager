import sqlite3 as sql
import tkinter as tk
from tkinter import ttk



def show_attendance():
    conn = sql.connect('user_database.db')
    c = conn.cursor()
    

    c.execute("SELECT * FROM attable")
    user_id = c.fetchone()

    if user_id:
    
        c.execute("SELECT * FROM attable")
        

        attendance_data = c.fetchall()

        for row in attendance_tree.get_children():
            attendance_tree.delete(row)

        for row in attendance_data:
             attendance_tree.insert('', 'end', values=row)
    else:
        print("User not found")
    
    conn.close()



root = tk.Tk()
root.title("Student Attendance Viewer")
width=1200
height=300
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)
        


attendance_tree = ttk.Treeview(root, columns=("Subject ID", "Subject", "Attended", "Bunked", "Percentage"))
attendance_tree.heading("#1", text="Subject ID")
attendance_tree.heading("#2", text="Subject")
attendance_tree.heading("#3", text="Attended")
attendance_tree.heading("#4", text="Bunked")
attendance_tree.heading("#5", text="Percentage")
attendance_tree.pack()


show_attendance_button = tk.Button(root, text="Show Attendance", command=show_attendance)
show_attendance_button.pack()

root.mainloop()
