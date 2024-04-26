import re
import csv
from datetime import datetime
from functools import lru_cache
import os

class Student:
    def __init__(self, id, name, dob, email, department, phone_number):
        self.id = id
        self.name = name
        self.dob = dob
        self.email = email
        self.department = department
        self.phone_number = phone_number
       

        # Validation logic
        if not re.match(r'^[A-Za-z.\s]{0,58}$', self.name):
            raise ValueError("Name must contain only letters and spaces, up to 60 characters")
        if not re.match(r'^[A-Za-z\s]+$', self.department):
            raise ValueError("Department must contain only letters and spaces")

        # Validate email format
        if not re.match(r'^\w+([.a-zAZ\s]?\w+)*@gmail.com$', self.email):
            raise ValueError("Email must end with @gmail.com")

        # Validate phone number format (example)
        if not re.match(r'^\d{10}$', self.phone_number):
            raise ValueError("Invalid phone number format, must contain exactly 10 digits")

        # Validate DOB and calculate age
        dob_date = datetime.strptime(self.dob, "%Y-%m-%d")
        age = datetime.now().year - dob_date.year - ((datetime.now().month, datetime.now().day) < (dob_date.month, dob_date.day))
        if age < 5 or age > 15:
            raise ValueError("Age must be between 5 and 15 years old")

class StudentModel:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    @lru_cache(maxsize=None)  # Cache all student records
    def get_all_students(self):
        students = []
        with open(self.csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append(row)
        return students

    def get_student_by_id(self, student_id):
        with open(self.csv_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                if row[0] == student_id:
                    return {
                        "ID": row[0],
                        "Name": row[1],
                        "DOB": row[2],
                        "Email": row[3],
                        "Department": row[4],
                        "Phone Number": row[5],
                      
                    }
        return None

    def get_student_by_email(self, email):
        with open(self.csv_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                if row[3] == email:
                    return {
                        "ID": row[0],
                        "Name": row[1],
                        "DOB": row[2],
                        "Email": row[3],
                        "Department": row[4],
                        "Phone Number": row[5],
                        
                    }
        return None

    def group_students_by_id(self):
        grouped_students = {"0-10": [], "11-20": [], "21-30": []}
        with open(self.csv_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                student_id = int(row[0])
                if 0 < student_id <= 10:
                    grouped_students["0-10"].append(row)
                elif 10 < student_id <= 20:
                    grouped_students["11-20"].append(row)
                elif 20 < student_id <= 30:
                    grouped_students["21-30"].append(row)
        return grouped_students

    def group_students_by_dob(self):
        grouped_students = {"0-10": [], "11-20": [], "21-30": []}
        with open(self.csv_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                dob_year = int(row[2].split("-")[0])
                if 0 < dob_year <= 2002:
                    grouped_students["0-10"].append(row)
                elif 2002 < dob_year <= 2012:
                    grouped_students["11-20"].append(row)
                elif 2012 < dob_year <= 2022:
                    grouped_students["21-30"].append(row)
        return grouped_students
    
    def create_student(self, student):
        students = self.read_students()
        student_ids = [stu.id for stu in students]
        if student.id in student_ids:
            raise ValueError("Student ID already exists. Please enter a unique ID.")
        
        with open(self.csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([student.id, student.name, student.dob, student.email, student.department, student.phone_number])
    
    def read_students(self):
        students = []
        with open(self.csv_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                students.append(Student(*row))
        return students

    def update_student(self, student):
        temp_file = "temp.csv"
        with open(self.csv_file, mode='r') as file, open(temp_file, mode='w', newline='') as temp:
            reader = csv.reader(file)
            writer = csv.writer(temp)
            for row in reader:
                if row[0] == student.id:
                    row = [student.id, student.name, student.dob, student.email, student.department, student.phone_number]
                writer.writerow(row)
        import os
        os.remove(self.csv_file)
        os.rename(temp_file, self.csv_file)

    

    def delete_student_by_id(self, student_id):
        found = False
        temp_file = "temp.csv"
        with open(self.csv_file, mode='r') as file, open(temp_file, mode='w', newline='') as temp:
            reader = csv.reader(file)
            writer = csv.writer(temp)
            for row in reader:
                if row[0] == student_id:
                    found = True
                else:
                    writer.writerow(row)

        if found:
            import os
            os.remove(self.csv_file)
            os.rename(temp_file, self.csv_file)
            print("Student deleted successfully.")
        else:
            print(f"No such student with the ID {student_id}.")


    def delete_student_by_email(self, email):
        found = False
        temp_file = "temp.csv"
        with open(self.csv_file, mode='r') as file, open(temp_file, mode='w', newline='') as temp:
            reader = csv.reader(file)
            writer = csv.writer(temp)
            for row in reader:
                if row[3] == email:
                    found = True
                else:
                    writer.writerow(row)

        if found:
            import os
            os.remove(self.csv_file)
            os.rename(temp_file, self.csv_file)
            print("Student deleted successfully.")
        else:
            print(f"No such student with the email {email}.")


    def delete_students_in_id_range(self, start_id, end_id):
        found = False
        temp_file = "temp.csv"
        with open(self.csv_file, mode='r') as file, open(temp_file, mode='w', newline='') as temp:
            reader = csv.reader(file)
            writer = csv.writer(temp)
            for row in reader:
                student_id = int(row[0])
                if start_id <= student_id <= end_id:
                    found = True
                else:
                    writer.writerow(row)

        if found:
            import os
            os.remove(self.csv_file)
            os.rename(temp_file, self.csv_file)
            print("Students deleted successfully.")
        else:
            print(f"No such student found in the provided ID range {start_id} to {end_id}.")

    def delete_students_in_dob_range(self, start_dob, end_dob):
        found = False
        temp_file = "temp.csv"
        with open(self.csv_file, mode='r') as file, open(temp_file, mode='w', newline='') as temp:
            reader = csv.reader(file)
            writer = csv.writer(temp)
            for row in reader:
                student_dob = row[2]
                if start_dob <= student_dob <= end_dob:
                    found = True
                else:
                    writer.writerow(row)

        if found:
            import os
            os.remove(self.csv_file)
            os.rename(temp_file, self.csv_file)
            print("Students deleted successfully.")
        else:
            print(f"No such student found in the provided DOB range {start_dob} to {end_dob}.")


    def delete_student(self, id):
        temp_file = "temp.csv"
        with open(self.csv_file, mode='r') as file, open(temp_file, mode='w', newline='') as temp:
            reader = csv.reader(file)
            writer = csv.writer(temp)
            for row in reader:
                if row[0] != id:
                    writer.writerow(row)
        import os
        os.remove(self.csv_file)
        os.rename(temp_file, self.csv_file)
    
        
