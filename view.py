class StudentView:
    def display_students(self, students):
        print("Student Details:")
        for student in students:
            print("ID:", student.id)
            print("Name:", student.name)
            print("DOB:", student.dob)
            print("Email:", student.email)
            print("Department:", student.department)
            print("Phone Number:", student.phone_number) 
            print()

    def display_grouped_students(self, grouped_students, group_by):
        for key, value in grouped_students.items():
            if group_by == "ID":
                # Sort students by ID
                sorted_students = sorted(value, key=lambda student: int(student[0]))
            else:
                # Sort students by DOB
                sorted_students = sorted(value, key=lambda student: student[2])
            
            print(f"Students in group {group_by} {key}:")
            for student in sorted_students:
                print("ID:", student[0])
                print("Name:", student[1])
                print("DOB:", student[2])
                print("Email:", student[3])
                print("Department:", student[4])
                print("Phone Number:", student[5])
                print("")