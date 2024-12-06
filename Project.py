import mysql.connector
from tkinter import Tk, Label, Entry, Button, Listbox, Scrollbar, END, messagebox

# Database Setup
import mysql.connector # Define your connection details 
conn = mysql.connector.connect( host="your_host", user="your_username", password="your_password", database="your_database" ) 
cursor.execute(""" CREATE TABLE IF NOT EXISTS students ( roll_number INT PRIMARY KEY, name VARCHAR(100) NOT NULL, class VARCHAR(100) NOT NULL, marks INT NOT NULL ) """)

# Functions
def add_student():
    if roll_number_var.get() and name_var.get() and class_var.get() and marks_var.get():
        try:
            cursor.execute("INSERT INTO students (roll_number, name, class, marks) VALUES (?, ?, ?, ?)",
                           (int(roll_number_var.get()), name_var.get(), class_var.get(), int(marks_var.get())))
            conn.commit()
            messagebox.showinfo("Success", "Student added successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Roll Number already exists.")
    else:
        messagebox.showerror("Error", "All fields are required.")

def view_students():
    listbox.delete(0, END)
    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        listbox.insert(END, f"Roll: {row[0]} | Name: {row[1]} | Class: {row[2]} | Marks: {row[3]}")

def delete_student():
    if roll_number_var.get():
        cursor.execute("DELETE FROM students WHERE roll_number=?", (int(roll_number_var.get()),))
        conn.commit()
        messagebox.showinfo("Success", "Student deleted successfully!")
        #view_students()
    else:
        messagebox.showerror("Error", "Roll Number is required.")

def search_student():
    listbox.delete(0, END)
    if roll_number_var.get():
        cursor.execute("SELECT * FROM students WHERE roll_number=?", (int(roll_number_var.get()),))
    elif name_var.get():
        cursor.execute("SELECT * FROM students WHERE name LIKE ?", (f"%{name_var.get()}%",))
    else:
        messagebox.showerror("Error", "Enter Roll Number or Name to search.")
        return

    records = cursor.fetchall()
    if records:
        for row in records:
            listbox.insert(END, f"Roll: {row[0]} | Name: {row[1]} | Class: {row[2]} | Marks: {row[3]}")
    else:
        messagebox.showinfo("Info", "No records found.")

# Tkinter GUI Setup
root = Tk()
root.title("Student Management System")
root.geometry("500x500")

# Labels and Entry Widgets
Label(root, text="Roll Number").grid(row=0, column=0, padx=10, pady=5)
Label(root, text="Name").grid(row=1, column=0, padx=10, pady=5)
Label(root, text="Class").grid(row=2, column=0, padx=10, pady=5)
Label(root, text="Marks").grid(row=3, column=0, padx=10, pady=5)

roll_number_var = Entry(root)
name_var = Entry(root)
class_var = Entry(root)
marks_var = Entry(root)

roll_number_var.grid(row=0, column=1, pady=5)
name_var.grid(row=1, column=1, pady=5)
class_var.grid(row=2, column=1, pady=5)
marks_var.grid(row=3, column=1, pady=5)

# Buttons
Button(root, text="Add Student", command=add_student).grid(row=4, column=0, padx=10, pady=10)
Button(root, text="View Students", command=view_students).grid(row=4, column=1, padx=10, pady=10)
Button(root, text="Delete Student", command=delete_student).grid(row=5, column=0, padx=10, pady=10)
Button(root, text="Search Student", command=search_student).grid(row=5, column=1, padx=10, pady=10)

# Listbox with Scrollbar
listbox = Listbox(root, width=50, height=15)
listbox.grid(row=6, column=0, columnspan=2, pady=10)
scrollbar = Scrollbar(root)
scrollbar.grid(row=6, column=2, sticky="ns")
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

root.mainloop()
