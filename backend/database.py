from pymongo import MongoClient
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["university_db"]

# Define collections
students_collection = db["students"]
faculty_collection = db["faculty"]
courses_collection = db["courses"]

# Sample departments
departments = ["Computer Science", "Electrical Engineering", "Mechanical Engineering", "Biotechnology", "Civil Engineering"]

# Sample subjects
subjects = {
    "Computer Science": ["Data Structures", "Algorithms", "Machine Learning", "Databases", "Operating Systems"],
    "Electrical Engineering": ["Circuits", "Electromagnetics", "Power Systems", "Embedded Systems", "Control Systems"],
    "Mechanical Engineering": ["Thermodynamics", "Fluid Mechanics", "Material Science", "Dynamics", "Robotics"],
    "Biotechnology": ["Genetics", "Microbiology", "Biochemistry", "Molecular Biology", "Bioinformatics"],
    "Civil Engineering": ["Structural Analysis", "Geotechnical Engineering", "Transportation Engineering", "Surveying", "Hydrology"]
}

# Generate sample student data
def generate_students(n=50):
    students = []
    for _ in range(n):
        department = random.choice(departments)
        student = {
            "name": fake.name(),
            "age": random.randint(18, 25),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "address": fake.address(),
            "marks": random.randint(50, 100),
            "GPA": round(random.uniform(2.5, 4.0), 2),
            "department": department,
            "enrollment_year": random.randint(2018, 2024),
            "subjects": random.sample(subjects[department], k=random.randint(2, 4)),
            "scholarship": random.choice([True, False])
        }
        students.append(student)
    return students

# Generate sample faculty data
def generate_faculty(n=20):
    faculty = []
    for _ in range(n):
        department = random.choice(departments)
        faculty_member = {
            "name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "department": department,
            "designation": random.choice(["Professor", "Assistant Professor", "Lecturer", "HOD"]),
            "years_of_experience": random.randint(3, 30),
            "research_area": fake.word(),
            "office_location": fake.address()
        }
        faculty.append(faculty_member)
    return faculty

# Generate sample course data
def generate_courses():
    courses = []
    for department in departments:
        for subject in subjects[department]:
            course = {
                "course_name": subject,
                "department": department,
                "course_code": f"{department[:3].upper()}-{random.randint(100, 500)}",
                "credits": random.randint(3, 5),
                "semester": random.randint(1, 8),
                "professor": fake.name()
            }
            courses.append(course)
    return courses

# Insert sample data if collections are empty
if students_collection.count_documents({}) == 0:
    students_collection.insert_many(generate_students())

if faculty_collection.count_documents({}) == 0:
    faculty_collection.insert_many(generate_faculty())

if courses_collection.count_documents({}) == 0:
    courses_collection.insert_many(generate_courses())

print("Sample university data inserted successfully!")
