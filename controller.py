import sys
print(sys.path)
import csv
from os import path
from model import StudentModel
from view import StudentView
from model import Student 
 # If Student is defined in a separate file within the model directory

# Define the CSV file path
CSV_FILE = "student.csv"

# Function to create a new CSV file if it doesn't exist
def create_csv_file():
    if not path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Name', 'DOB', 'Email', 'Department', 'Phone Number', 'Status'])
        print(f"CSV file '{CSV_FILE}' created successfully.")

class StudentController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def create_student(self, id, name, dob, email, department, phone_number):
        student = Student(id, name, dob, email, department, phone_number)
        self.model.create_student(student)

    def read_students(self):
        students = self.model.read_students()
        self.view.display_students(students)

    def update_student(self, id, name, dob, email, department, phone_number):
        student = Student(id, name, dob, email, department, phone_number)
        self.model.update_student(student)

    def delete_student(self, id):
        self.model.delete_student(id)
    
    def read_students_pagination(self):
        students = self.model.read_students()
        page_size = 10
        num_pages = (len(students) + page_size - 1) // page_size

        page_number = 1
        while True:
            start_index = (page_number - 1) * page_size
            end_index = min(start_index + page_size, len(students))

            current_page_students = students[start_index:end_index]
            self.view.display_students(current_page_students)

            print(f"Page {page_number} of {num_pages}")

            if page_number == 1 and num_pages > 1:
                print("Enter '>' for next page")
            elif page_number > 1 and page_number < num_pages:
                print("Enter '<' for previous page, or '>' for next page")
            elif page_number == num_pages:
                print("Enter '<' for previous page")

            user_input = input("Enter your choice: ")

            if user_input == ">":
                if page_number < num_pages:
                    page_number += 1
                else:
                    print("Already on the last page.")
            elif user_input == "<":
                if page_number > 1:
                    page_number -= 1
                else:
                    print("Already on the first page.")
            else:
                break 

def main():
    create_csv_file()  # Ensure the CSV file is created
    model = StudentModel(CSV_FILE)
    view = StudentView()
    controller = StudentController(model, view)


   

if __name__ == "__main__":
    main()
