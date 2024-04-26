import csv
from os import path
import model
import view
import re
from controller import StudentController
from model import StudentModel
from view import StudentView
from datetime import datetime

# Define the CSV file path
CSV_FILE = "student.csv"

# Function to create a new CSV file if it doesn't exist
def create_csv_file():
    if not path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Name', 'DOB', 'Email', 'Department', 'Phone Number'])
        print(f"CSV file '{CSV_FILE}' created successfully.")

def is_unique_id(id):
    with open(CSV_FILE, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            if row[0] == id:
                return False
    return True
def is_unique_email(email):
    with open(CSV_FILE, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            if row[3] == email:
                return False
    return True

def main():
    create_csv_file()  # Ensure the CSV file is created
    model_instance = StudentModel(CSV_FILE)
    view_instance = StudentView()
    controller = StudentController(model_instance, view_instance)

    while True:
        print("\nStudent CRUD Operations")
        print("1. Create Student")
        print("2. Read Student List")
        print("3. Update Student Details")
        print("4. Delete Student")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            while True:
                id = input("Enter student ID: ")
                if not is_unique_id(id):
                    print("ID already exists. Please enter a unique ID.")
                    continue  # Continue the loop to prompt for a new ID
                else:
                    break  # Break the loop if the ID is unique

            while True:
                name = input("Enter student name: ")
                if not re.match(r'^[a-zA-Z. ]+$', name):
                    print("Name must contain only letters, spaces, and periods.")
                    continue
                else:
                    break  

            while True:
                dob = input("Enter student DOB (YYYY-MM-DD): ")
                # Validate DOB format
                try:
                    dob_date = datetime.strptime(dob, "%Y-%m-%d")
                    # Calculate age
                    age = datetime.now().year - dob_date.year - ((datetime.now().month, datetime.now().day) < (dob_date.month, dob_date.day))
                    # Check age range
                    if age < 5 or age > 15:
                        print("Age must be between 5 and 15 years old.")
                        continue
                    else:
                        break  # Break the loop if DOB is valid
                except ValueError:
                    print("Invalid date format. Please enter date in YYYY-MM-DD format.")
                    continue

            while True:
                email = input("Enter student email: ")
                # Validate email format
                if not re.match(r'^\w+([.a-zAZ\s]?\w+)*@gmail.com$', email):
                    print("Email must end with @gmail.com")
                    continue
                elif not is_unique_email(email):
                    print("Email already exists. Please enter a unique email.")
                    continue
                else:
                    break # Break the loop if email is valid

            while True:
                department = input("Enter student department: ")
                if not department.isalpha():
                    print("Department must contain only letters.")
                    continue
                else:
                    break  # Break the loop if department is valid

            while True:
                phone_number = input("Enter student phone number: ")
                # Validate phone number format
                if not phone_number.isdigit() or len(phone_number) != 10:
                    print("Invalid phone number format. Please enter exactly 10 digits.")
                    continue
                else:
                    break  # Break the loop if phone number is valid

            # Create the student if all validations pass
            controller.create_student(id, name, dob, email, department, phone_number)

        elif choice == "2":
            read_option = input("Choose read option (1: StudentID/Email, 2: Group display of ID/DOB, 3: ALL Pagination): ")
            if read_option == "1":
                id_or_email = input("Enter Student ID or Email: ")
                if id_or_email.isdigit():
                    student_data = model_instance.get_student_by_id(id_or_email)
                else:
                    student_data = model_instance.get_student_by_email(id_or_email)
                if student_data:
                    student = model.Student(*student_data.values())
                    view_instance.display_students([student])
                else:
                    print("Student not found.")
            elif read_option == "2":
                group_option = input("Choose group option (1: Group display by ID, 2: Group display by DOB): ")
                if group_option == "1":
                    students_by_id_group = model_instance.group_students_by_id()
                    view_instance.display_grouped_students(students_by_id_group, group_by="ID")
                elif group_option == "2":
                    students_by_dob_group = model_instance.group_students_by_dob()
                    view_instance.display_grouped_students(students_by_dob_group, group_by="DOB")
                else:
                    print("Invalid group option.")
            elif read_option == "3":
                controller.read_students_pagination()
            else:
                print("Invalid read option.")
        
        elif choice == "3":
            id = input("Enter student ID to update: ")
            if not is_unique_id(id):
                print("ID does not exist. Please enter a valid ID.")
                continue
            # Fetch the student details
            student = model_instance.get_student_by_id(id)
            if student is None:
                print("Student not found.")
                continue

            # Display current student details
            print("Current Student Details:")
            view_instance.display_students([student])

            # Prompt for updated details
            print("\nEnter updated student details:")
            while True:
                name = input("Enter student name: ")
                if not re.match(r'^[a-zA-Z. ]+$', name):
                    print("Name must contain only letters, spaces, and periods.")
                    continue
                else:
                    break  

            while True:
                dob = input("Enter student DOB (YYYY-MM-DD): ")
                # Validate DOB format
                try:
                    dob_date = datetime.strptime(dob, "%Y-%m-%d")
                    # Calculate age
                    age = datetime.now().year - dob_date.year - ((datetime.now().month, datetime.now().day) < (dob_date.month, dob_date.day))
                    # Check age range
                    if age < 5 or age > 15:
                        print("Age must be between 5 and 15 years old.")
                        continue
                    else:
                        break  # Break the loop if DOB is valid
                except ValueError:
                    print("Invalid date format. Please enter date in YYYY-MM-DD format.")
                    continue

            while True:
                email = input("Enter student email: ")
                # Validate email format
                if not re.match(r'^\w+([.a-zAZ\s]?\w+)*@gmail.com$', email):
                    print("Email must end with @gmail.com")
                    continue
                elif not is_unique_email(email):
                    print("Email already exists. Please enter a unique email.")
                    continue
                else:
                    break   # Break the loop if email is valid

            while True:
                department = input("Enter student department: ")
                if not department.isalpha():
                    print("Department must contain only letters.")
                    continue
                else:
                    break  # Break the loop if department is valid

            while True:
                phone_number = input("Enter student phone number: ")
                # Validate phone number format
                if not phone_number.isdigit() or len(phone_number) != 10:
                    print("Invalid phone number format. Please enter exactly 10 digits.")
                    continue
                else:
                    break  # Break the loop if phone number is valid

            # Update the student if all validations pass
            controller.update_student(id, name, dob, email, department, phone_number)

        elif choice == "4":
            delete_option = input("Choose delete option (1: Delete by ID, 2: Delete by Email, 3: Delete by ID Range, 4: Delete by DOB Range): ")
            if delete_option == "1":
                student_id = input("Enter student ID to delete: ")
                controller.delete_student_by_id(student_id)
                print("Student deleted successfully.")
            elif delete_option == "2":
                email = input("Enter student email to delete: ")
                controller.delete_student_by_email(email)
                print("Student deleted successfully.")
            elif delete_option == "3":
                start_id = int(input("Enter starting ID of the range: "))
                end_id = int(input("Enter ending ID of the range: "))
                controller.delete_students_in_id_range(start_id, end_id)
                print("Students in the ID range deleted successfully.")
            elif delete_option == "4":
                start_dob = input("Enter starting date of birth (YYYY-MM-DD) of the range: ")
                end_dob = input("Enter ending date of birth (YYYY-MM-DD) of the range: ")
                controller.delete_students_in_dob_range(start_dob, end_dob)
                print("Students in the DOB range deleted successfully.")
            else:
                print("Invalid delete option.")

        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
