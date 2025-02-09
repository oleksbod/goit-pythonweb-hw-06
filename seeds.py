from sqlalchemy.orm import Session
from faker import Faker
import random
from connectdb import engine
from models import Group, Student, Teacher, Subject, Grade
from datetime import datetime

# Константи для груп і предметів
GROUP_NAMES = ["Group A", "Group B", "Group C"]
SUBJECT_NAMES = ["Mathematics", "Physics", "Chemistry", "Biology", "History", "Geography", "English", "Computer Science"]

def seed_database():
    fake = Faker()
    session = Session(engine)   
    
    # Створення Groups
    groups = [Group(name=name) for name in GROUP_NAMES]
    session.add_all(groups)
    session.commit()
    
    # Створення Teachers
    teachers = [Teacher(name=fake.name()) for _ in range(random.randint(3, 5))]
    session.add_all(teachers)
    session.commit()
    
    # Створення Subjects
    subjects = [Subject(name=name, teacher=random.choice(teachers)) for name in random.sample(SUBJECT_NAMES, random.randint(5, 8))]
    session.add_all(subjects)
    session.commit()
    
    # Створення Students
    students = []
    for _ in range(30):
        student = Student(
            name=fake.name(),
            email=fake.email(),
            group=random.choice(groups)
        )
        students.append(student)
    session.add_all(students)
    session.commit()
    
    # Створення Grades
    grades = []
    for student in students:
        for subject in subjects:
            for _ in range(random.randint(10, 20)):
                grade = Grade(
                    mark=random.randint(1, 10),
                    date_received=fake.date_this_year(),
                    student=student,
                    subject=subject
                )
                grades.append(grade)
    session.add_all(grades)
    session.commit()
    
    session.close()
    print("Database seeding completed!")

if __name__ == "__main__":
    seed_database()
