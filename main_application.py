"""
================================================================================
            SMART CAMPUS INFORMATION SYSTEM  -  main_application.py
                        (Lab 9 & 10 : Mini Project Integration)
================================================================================
A single menu-driven Python application that integrates all the modules built
from Lab 1 to Lab 8 into one Smart Campus Information System dashboard:

    Lab 1  Student Registration & Grade Evaluation
    Lab 2  Course Enrollment Management
    Lab 3  Student Records Management
    Lab 4  Searching and Sorting Student Data
    Lab 5  Fee Calculation using Functions
    Lab 6  File-based Academic Record Management (CSV)
    Lab 7  Directory Scanning with Exception Handling
    Lab 8  Student Performance Analytics (NumPy, Pandas, Matplotlib)

Authors : Jeel S Vaghasiya (1DS25CG021)
          Jigyasu Tanwar  (1DS25CG022)
================================================================================
"""

import os
import csv
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")               # headless backend so charts save without a GUI
import matplotlib.pyplot as plt

RECORD_FILE = "student_records.csv"

# Master list of student records held in memory while the program runs.
# Each record is a dictionary with these keys:
#   usn, name, sub1, sub2, sub3, average, grade, course, fee
students = []

# Courses offered on campus and their additional fee (Lab 2 / Lab 5)
COURSES = {
    "1": ("Python Programming", 5000),
    "2": ("Data Structures", 6000),
    "3": ("Web Development", 5500),
    "4": ("Machine Learning", 8000),
}
BASE_FEE = 40000                    # common college base fee


# ============================================================================ #
#  LAB 6 : FILE-BASED ACADEMIC RECORD MANAGEMENT
# ============================================================================ #
def save_records():
    """Write every student record to a CSV file."""
    fields = ["usn", "name", "sub1", "sub2", "sub3",
              "average", "grade", "course", "fee"]
    with open(RECORD_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(students)


def load_records():
    """Load student records from the CSV file if it exists, else seed demo data."""
    global students
    if os.path.exists(RECORD_FILE):
        with open(RECORD_FILE, "r", newline="") as f:
            reader = csv.DictReader(f)
            students = []
            for row in reader:
                for k in ("sub1", "sub2", "sub3", "fee"):
                    row[k] = int(row[k])
                row["average"] = float(row["average"])
                students.append(row)
    else:
        seed_demo_data()
        save_records()


def seed_demo_data():
    """Create a few sample records so the system is usable on first run."""
    samples = [
        ("1DS25CG021", "Jeel S Vaghasiya", 88, 92, 85, "Python Programming"),
        ("1DS25CG022", "Jigyasu Tanwar", 79, 81, 76, "Data Structures"),
        ("1DS25CG023", "Aarav Mehta", 65, 58, 70, "Web Development"),
        ("1DS25CG024", "Diya Nair", 91, 95, 89, "Machine Learning"),
    ]
    for usn, name, s1, s2, s3, course in samples:
        avg = (s1 + s2 + s3) / 3
        students.append({
            "usn": usn, "name": name, "sub1": s1, "sub2": s2, "sub3": s3,
            "average": round(avg, 2), "grade": evaluate_grade(avg),
            "course": course, "fee": calculate_fee(course),
        })


# ============================================================================ #
#  LAB 5 : FEE CALCULATION USING FUNCTIONS
# ============================================================================ #
def calculate_fee(course_name):
    """Return total fee = base fee + the course-specific fee."""
    course_fee = 0
    for _, (name, fee) in COURSES.items():
        if name == course_name:
            course_fee = fee
            break
    return BASE_FEE + course_fee


# ============================================================================ #
#  LAB 1 : STUDENT REGISTRATION & GRADE EVALUATION
# ============================================================================ #
def evaluate_grade(average):
    """Map an average mark to a letter grade."""
    if average >= 90:
        return "A+"
    elif average >= 75:
        return "A"
    elif average >= 60:
        return "B"
    elif average >= 40:
        return "C"
    return "FAIL"


def register_student():
    print("\n--- Student Registration & Grade Evaluation ---")
    usn = input("  Enter USN              : ").strip().upper()
    if any(s["usn"] == usn for s in students):
        print("  ! A student with this USN already exists.")
        return
    name = input("  Enter Name             : ").strip()
    try:
        s1 = int(input("  Marks in Subject 1     : "))
        s2 = int(input("  Marks in Subject 2     : "))
        s3 = int(input("  Marks in Subject 3     : "))
    except ValueError:
        print("  ! Marks must be whole numbers. Registration cancelled.")
        return
    average = round((s1 + s2 + s3) / 3, 2)
    grade = evaluate_grade(average)
    students.append({
        "usn": usn, "name": name, "sub1": s1, "sub2": s2, "sub3": s3,
        "average": average, "grade": grade, "course": "Not enrolled", "fee": 0,
    })
    save_records()
    print(f"  > Registered. Average = {average}, Grade = {grade}")


# ============================================================================ #
#  LAB 2 : COURSE ENROLLMENT MANAGEMENT
# ============================================================================ #
def enroll_course():
    print("\n--- Course Enrollment Management ---")
    usn = input("  Enter student USN : ").strip().upper()
    student = next((s for s in students if s["usn"] == usn), None)
    if not student:
        print("  ! No student found with that USN.")
        return
    print("  Available Courses:")
    for key, (name, fee) in COURSES.items():
        print(f"    {key}. {name}  (Course Fee: Rs.{fee})")
    choice = input("  Choose course number : ").strip()
    if choice not in COURSES:
        print("  ! Invalid course choice.")
        return
    course_name = COURSES[choice][0]
    student["course"] = course_name
    student["fee"] = calculate_fee(course_name)
    save_records()
    print(f"  > {student['name']} enrolled in {course_name}. "
          f"Total fee: Rs.{student['fee']}")


# ============================================================================ #
#  LAB 3 : STUDENT RECORDS MANAGEMENT
# ============================================================================ #
def display_record(s):
    print(f"  {s['usn']:12} | {s['name']:18} | Avg: {s['average']:6} | "
          f"Grade: {s['grade']:4} | {s['course']:18} | Fee: Rs.{s['fee']}")


def view_records():
    print("\n--- Student Records ---")
    if not students:
        print("  No records available.")
        return
    print("  " + "-" * 92)
    for s in students:
        display_record(s)
    print("  " + "-" * 92)


def delete_record():
    print("\n--- Delete Student Record ---")
    usn = input("  Enter USN to delete : ").strip().upper()
    global students
    before = len(students)
    students = [s for s in students if s["usn"] != usn]
    if len(students) < before:
        save_records()
        print("  > Record deleted.")
    else:
        print("  ! USN not found.")


# ============================================================================ #
#  LAB 4 : SEARCHING AND SORTING STUDENT DATA
# ============================================================================ #
def search_student():
    print("\n--- Search Student ---")
    key = input("  Enter USN or Name : ").strip().lower()
    found = [s for s in students
             if key in s["usn"].lower() or key in s["name"].lower()]
    if not found:
        print("  ! No matching student found.")
        return
    for s in found:
        display_record(s)


def sort_students():
    print("\n--- Sort Students ---")
    print("  1. By Name (A-Z)   2. By Average (high to low)")
    ch = input("  Choice : ").strip()
    if ch == "1":
        ordered = sorted(students, key=lambda s: s["name"])
    elif ch == "2":
        ordered = sorted(students, key=lambda s: s["average"], reverse=True)
    else:
        print("  ! Invalid choice.")
        return
    for s in ordered:
        display_record(s)


# ============================================================================ #
#  LAB 7 : DIRECTORY SCANNING WITH EXCEPTION HANDLING
# ============================================================================ #
def scan_directory():
    print("\n--- Directory Scanner ---")
    path = input("  Enter directory path (blank = current) : ").strip() or "."
    try:
        items = os.listdir(path)
        py_files = [f for f in items if f.endswith(".py")]
        csv_files = [f for f in items if f.endswith(".csv")]
        print(f"  Scanned: {os.path.abspath(path)}")
        print(f"  Total items : {len(items)}")
        print(f"  Python files: {py_files if py_files else 'None'}")
        print(f"  CSV files   : {csv_files if csv_files else 'None'}")
    except FileNotFoundError:
        print("  ! Error: that directory does not exist.")
    except PermissionError:
        print("  ! Error: permission denied for that directory.")
    except Exception as e:
        print(f"  ! Unexpected error: {e}")


# ============================================================================ #
#  LAB 8 : STUDENT PERFORMANCE ANALYTICS (NumPy, Pandas, Matplotlib)
# ============================================================================ #
def performance_analytics():
    print("\n--- Student Performance Analytics ---")
    if not students:
        print("  No records to analyse.")
        return

    # Pandas: build a DataFrame from the records
    df = pd.DataFrame(students)
    averages = np.array(df["average"], dtype=float)   # NumPy array

    # NumPy: summary statistics
    print(f"  Number of students : {len(df)}")
    print(f"  Class mean average : {np.mean(averages):.2f}")
    print(f"  Highest average    : {np.max(averages):.2f}")
    print(f"  Lowest average     : {np.min(averages):.2f}")
    print(f"  Standard deviation : {np.std(averages):.2f}")

    topper = df.loc[df["average"].idxmax()]
    print(f"  Class topper       : {topper['name']} ({topper['average']})")

    # Matplotlib: bar chart of each student's average, saved to a PNG file
    plt.figure(figsize=(8, 4.5))
    plt.bar(df["name"], df["average"], color="#2E75B6")
    plt.axhline(np.mean(averages), color="red", linestyle="--",
                label=f"Class mean ({np.mean(averages):.1f})")
    plt.title("Student Performance - Average Marks")
    plt.xlabel("Student")
    plt.ylabel("Average Marks")
    plt.xticks(rotation=20, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig("performance_chart.png", dpi=120)
    plt.close()
    print("  > Performance chart saved as 'performance_chart.png'.")


# ============================================================================ #
#  MAIN SYSTEM APPLICATION DASHBOARD (Lab 9 & 10)
# ============================================================================ #
def main():
    load_records()
    print("=" * 70)
    print("            SMART CAMPUS INFORMATION SYSTEM - DASHBOARD")
    print("=" * 70)

    menu = """
----------------------------------------------------------------------
                         MAIN MENU
----------------------------------------------------------------------
  1. Student Registration & Grade Evaluation      (Lab 1)
  2. Course Enrollment Management                  (Lab 2)
  3. View Student Records                          (Lab 3)
  4. Delete Student Record                         (Lab 3)
  5. Search Student                                (Lab 4)
  6. Sort Students                                 (Lab 4)
  7. Fee Details (per student)                     (Lab 5)
  8. Scan Directory for Project Files              (Lab 7)
  9. Performance Analytics                         (Lab 8)
 10. Exit
----------------------------------------------------------------------"""

    while True:
        print(menu)
        choice = input("  Enter your choice : ").strip()
        if choice == "1":
            register_student()
        elif choice == "2":
            enroll_course()
        elif choice == "3":
            view_records()
        elif choice == "4":
            delete_record()
        elif choice == "5":
            search_student()
        elif choice == "6":
            sort_students()
        elif choice == "7":
            show_fee_details()
        elif choice == "8":
            scan_directory()
        elif choice == "9":
            performance_analytics()
        elif choice == "10":
            print("\n  Records saved to file. Thank you! Goodbye.")
            break
        else:
            print("  ! Invalid choice. Please try again.")


def show_fee_details():
    print("\n--- Fee Details ---")
    usn = input("  Enter USN : ").strip().upper()
    student = next((s for s in students if s["usn"] == usn), None)
    if not student:
        print("  ! USN not found.")
        return
    print(f"  Student : {student['name']}")
    print(f"  Course  : {student['course']}")
    print(f"  Base Fee   : Rs.{BASE_FEE}")
    print(f"  Total Fee  : Rs.{student['fee']}")


if __name__ == "__main__":
    main()
