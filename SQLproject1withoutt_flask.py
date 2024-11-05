import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime

# Database connection function
def db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="omenHP@199",
        database="OnlineCourseManagement"
    )

# Main Application

root = tk.Tk()
root.title("Online Course Management System")
root.geometry("700x500")
root.config(bg="lightblue")

# Frame to display courses
course_frame = tk.Frame(root)
course_frame.pack(pady=20)


# Function to show available courses
def show_courses():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT CourseID, CourseName FROM Courses")
    courses = cursor.fetchall()
    conn.close()
    
    for widget in course_frame.winfo_children():
        widget.destroy()

    for course in courses:
        tk.Label(course_frame, text=f"Course ID: {course[0]} - {course[1]}").pack()

# Function to enroll a student
def enroll_student():
    def submit_enrollment():
        conn = db_connection()
        cursor = conn.cursor()

        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        email = email_entry.get()
        course_id = course_id_entry.get()

        cursor.execute("INSERT INTO Students (FirstName, LastName, Email, EnrollmentDate) VALUES (%s, %s, %s, %s)",
                       (first_name, last_name, email, datetime.now().date()))
        student_id = cursor.lastrowid

        cursor.execute("INSERT INTO Enrollments (StudentID, CourseID, EnrollmentDate) VALUES (%s, %s, %s)",
                       (student_id, course_id, datetime.now().date()))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", f"Student {first_name} enrolled in course ID {course_id} successfully!")
        enrollment_window.destroy()

    # Enrollment Form
    enrollment_window = tk.Toplevel(root)
    enrollment_window.title("Enroll Student")

    tk.Label(enrollment_window, text="First Name").pack()
    first_name_entry = tk.Entry(enrollment_window)
    first_name_entry.pack()

    tk.Label(enrollment_window, text="Last Name").pack()
    last_name_entry = tk.Entry(enrollment_window)
    last_name_entry.pack()

    tk.Label(enrollment_window, text="Email").pack()
    email_entry = tk.Entry(enrollment_window)
    email_entry.pack()

    tk.Label(enrollment_window, text="Course ID").pack()
    course_id_entry = tk.Entry(enrollment_window)
    course_id_entry.pack()

    tk.Button(enrollment_window, text="Enroll", command=submit_enrollment).pack()

# Function to view enrollments
def view_enrollments():
    enrollments_window = tk.Toplevel(root)
    enrollments_window.title("Enrollments")

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Students.FirstName, Students.LastName, Courses.CourseName, Enrollments.EnrollmentDate "
                   "FROM Enrollments "
                   "JOIN Students ON Enrollments.StudentID = Students.StudentID "
                   "JOIN Courses ON Enrollments.CourseID = Courses.CourseID")
    enrollments = cursor.fetchall()
    conn.close()

    for enrollment in enrollments:
        tk.Label(enrollments_window, text=f"Student: {enrollment[0]} {enrollment[1]}, Course: {enrollment[2]}, "
                                          f"Date: {enrollment[3]}").pack()

# Button to show courses
tk.Button(root, text="Show Courses", command=show_courses).pack(pady=5)

# Button to enroll a student
tk.Button(root, text="Enroll Student", command=enroll_student).pack(pady=5)

# Button to view enrollments
tk.Button(root, text="View Enrollments", command=view_enrollments).pack(pady=5)

# Run the main loop
root.mainloop()
