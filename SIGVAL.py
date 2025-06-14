"""
SIGVAL
by Melissa Espitia
"""
import os
import sys

def main():

    # Set of students: each student is a tuple (student_code, student_name)
    students = set()

    # Set of professors: each professor is a tuple (professor_id, professor_name)
    professors = set()

    # Set of courses: each course is a tuple (course_id, course_name, group)
    courses = set()

    # Set of course schedules: each item is a tuple (course_id, group, time_block)
    course_schedules = set()

    # Set of course professors: each item is a tuple (course_id, group, professor_id)
    course_professors = set()

    # Set of student enrollments: each item is a tuple (student_code, course_id, group)
    student_enrollments = set()

    
    def reg_student(student_code, student_name):
        """Add a new student as (code, name) tuple."""
        students.add((student_code, student_name))

    def remove_student(student_code):
        """Remove a student and all their enrollments."""
        nonlocal students, student_enrollments
        to_remove = {s for s in students if s[0] == student_code}
        students.difference_update(to_remove)
        enrollments_to_remove = {e for e in student_enrollments if e[0] == student_code}
        student_enrollments.difference_update(enrollments_to_remove)

    # CRUD for courses
    def add_course(course_id, course_name, group):
        """Add a new course as (id, name, group) tuple."""
        courses.add((course_id, course_name, group))

    def remove_course(course_id, group):
        """Remove a course and all related schedules, professors, and enrollments."""
        nonlocal courses, course_schedules, course_professors, student_enrollments
        to_remove = {c for c in courses if c[0] == course_id and c[2] == group}
        courses.difference_update(to_remove)
        course_schedules.difference_update({cs for cs in course_schedules if cs[0] == course_id and cs[1] == group})
        course_professors.difference_update({cp for cp in course_professors if cp[0] == course_id and cp[1] == group})
        student_enrollments.difference_update({e for e in student_enrollments if e[1] == course_id and e[2] == group})

    
    def enroll_student_in_course(student_code, course_id, group):
        """Enroll a student in a course group if there is no schedule conflict."""
        enrolled = {(cid, grp) for scode, cid, grp in student_enrollments if scode == student_code}
        new_course_blocks = {tb for cid, grp, tb in course_schedules if cid == course_id and grp == group}
        for cid, grp in enrolled:
            existing_blocks = {tb for c, g, tb in course_schedules if c == cid and g == grp}
            if new_course_blocks.intersection(existing_blocks):
                print("Schedule conflict for student!")
                return False  # Conflict
        student_enrollments.add((student_code, course_id, group))
        print("Enrollment successful.")
        return True

    def remove_student_enrollment(student_code, course_id, group):
        """Remove a student's enrollment from a course group."""
        nonlocal student_enrollments
        to_remove = {e for e in student_enrollments if e[0] == student_code and e[1] == course_id and e[2] == group}
        student_enrollments.difference_update(to_remove)

    
    def add_professor(professor_id, professor_name):
        """Add a new professor as (id, name) tuple."""
        professors.add((professor_id, professor_name))

    def remove_professor(professor_id):
        """Remove a professor and all their course assignments."""
        nonlocal professors, course_professors
        professors.difference_update({p for p in professors if p[0] == professor_id})
        course_professors.difference_update({cp for cp in course_professors if cp[2] == professor_id})

    def assign_professor_to_course(course_id, group, professor_id):
        """Assign a professor to a course group if there is no schedule conflict."""
        assigned = {(cid, grp) for cid, grp, pid in course_professors if pid == professor_id}
        new_course_blocks = {tb for cid, grp, tb in course_schedules if cid == course_id and grp == group}
        for cid, grp in assigned:
            existing_blocks = {tb for c, g, tb in course_schedules if c == cid and g == grp}
            if new_course_blocks.intersection(existing_blocks):
                print("Schedule conflict for professor!")
                return False  # Conflict
        course_professors.add((course_id, group, professor_id))
        print("Professor assigned successfully.")
        return True

    def remove_professor_from_course(course_id, group, professor_id):
        """Remove a professor from a course group."""
        nonlocal course_professors
        to_remove = {cp for cp in course_professors if cp[0] == course_id and cp[1] == group and cp[2] == professor_id}
        course_professors.difference_update(to_remove)

    
    def add_course_schedule(course_id, group, time_block):
        """Assign a time block to a course group."""
        course_schedules.add((course_id, group, time_block))

    def remove_course_schedule(course_id, group, time_block):
        """Remove a time block from a course group."""
        nonlocal course_schedules
        to_remove = {cs for cs in course_schedules if cs[0] == course_id and cs[1] == group and cs[2] == time_block}
        course_schedules.difference_update(to_remove)

    # Preload example data
    students.update({
        ("20230001", "Ana Torres"),
        ("20230002", "Luis Pérez"),
        ("20230003", "María Ruiz"),
        ("20230004", "Carlos Díaz"),
        ("20230005", "Sofía Gómez"),
        ("20230006", "Juan Ríos"),
    })

    professors.update({
        ("P001", "Dr. Ramírez"),
        ("P002", "Dra. Salazar"),
        ("P003", "Dr. Mendoza"),
    })

    courses.update({
        ("MAT101", "Discrete Math", "01"),
        ("MAT102", "Algebra", "01"),
        ("MAT103", "Calculus", "01"),
        ("MAT104", "Logic", "01"),
    })

    course_schedules.update({
        ("MAT101", "01", "Mon9-11"),
        ("MAT102", "01", "Mon9-11"),
        ("MAT103", "01", "Tue9-11"),
        ("MAT104", "01", "Wed9-11"),
    })

    course_professors.update({
        ("MAT101", "01", "P001"),
        ("MAT102", "01", "P002"),
        ("MAT103", "01", "P003"),
        ("MAT104", "01", "P001"),
    })

    student_enrollments.update({
        ("20230001", "MAT101", "01"),
        ("20230001", "MAT103", "01"),
        ("20230002", "MAT101", "01"),
        ("20230003", "MAT104", "01"),
        ("20230004", "MAT102", "01"),
        ("20230005", "MAT103", "01"),
        ("20230006", "MAT104", "01"),
    })

    def view_courses_and_enrollments():
        """Show all courses, their students and assigned professor."""
        print("\n" + "="*40)
        print("           COURSES AND ENROLLMENTS")
        print("="*40)
        for course in sorted(courses):
            course_id, course_name, group = course
            print(f"\nCourse: {course_id} - {course_name} | Group: {group}")
            # Find professor(s) assigned
            profs = [cp[2] for cp in course_professors if cp[0] == course_id and cp[1] == group]
            if profs:
                # Get professor names
                prof_names = []
                for pid in profs:
                    name = next((n for p, n in professors if p == pid), "Unknown")
                    prof_names.append(f"{pid} ({name})")
                print("Professor(s): " + ", ".join(prof_names))
            else:
                print("Professor(s): None assigned")
            # Find students enrolled
            enrolled = [s for s in student_enrollments if s[1] == course_id and s[2] == group]
            if enrolled:
                print("Enrolled students:")
                for scode, _, _ in enrolled:
                    name = next((n for c, n in students if c == scode), "Unknown")
                    print(f"  - {scode} | {name}")
            else:
                print("Enrolled students: None")
            # Show schedule
            scheds = [tb for cid, grp, tb in course_schedules if cid == course_id and grp == group]
            if scheds:
                print("Schedule: " + ", ".join(scheds))
            else:
                print("Schedule: Not assigned")
            print("-"*40)

    # Menu loop
    while True:
        print("\n" + "="*40)
        print("      SIGVAL - University Management System")
        print("="*40)
        print("1. Register student")
        print("2. Register professor")
        print("3. Register course")
        print("4. Assign schedule to course")
        print("5. Assign professor to course")
        print("6. Enroll student in course")
        print("7. Remove student enrollment")
        print("8. Remove student")
        print("9. Remove course")
        print("10. Remove professor")
        print("11. Remove professor from course")
        print("12. Remove schedule from course group")
        print("13. View all courses and enrollments")
        print("0. Exit")
        print("="*40)
        option = input("Select an option: ")

        if option == "1":
            code = input("Student code: ")
            name = input("Student name: ")
            reg_student(code, name)
            print("Student registered.")
        elif option == "2":
            pid = input("Professor ID: ")
            pname = input("Professor name: ")
            add_professor(pid, pname)
            print("Professor registered.")
        elif option == "3":
            cid = input("Course ID: ")
            cname = input("Course name: ")
            group = input("Group: ")
            add_course(cid, cname, group)
            print("Course registered.")
        elif option == "4":
            cid = input("Course ID: ")
            group = input("Group: ")
            tblock = input("Time block (e.g., Mon9-11): ")
            add_course_schedule(cid, group, tblock)
            print("Schedule assigned.")
        elif option == "5":
            cid = input("Course ID: ")
            group = input("Group: ")
            pid = input("Professor ID: ")
            assign_professor_to_course(cid, group, pid)
        elif option == "6":
            scode = input("Student code: ")
            cid = input("Course ID: ")
            group = input("Group: ")
            enroll_student_in_course(scode, cid, group)
        elif option == "7":
            scode = input("Student code: ")
            cid = input("Course ID: ")
            group = input("Group: ")
            remove_student_enrollment(scode, cid, group)
            print("Enrollment removed.")
        elif option == "8":
            scode = input("Student code: ")
            remove_student(scode)
            print("Student removed.")
        elif option == "9":
            cid = input("Course ID: ")
            group = input("Group: ")
            remove_course(cid, group)
            print("Course removed.")
        elif option == "10":
            pid = input("Professor ID: ")
            remove_professor(pid)
            print("Professor removed.")
        elif option == "11":
            cid = input("Course ID: ")
            group = input("Group: ")
            pid = input("Professor ID: ")
            remove_professor_from_course(cid, group, pid)
            print("Professor removed from course group.")
        elif option == "12":
            cid = input("Course ID: ")
            group = input("Group: ")
            tblock = input("Time block (e.g., Mon9-11): ")
            remove_course_schedule(cid, group, tblock)
            print("Schedule removed from course group.")
        elif option == "13":
            view_courses_and_enrollments()
        elif option == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
