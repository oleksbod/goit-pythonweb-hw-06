from sqlalchemy.orm import Session
from connectdb import engine
from models import Group, Student, Teacher, Subject, Grade
from sqlalchemy import func, desc
from seeds import GROUP_NAMES, SUBJECT_NAMES

"""
Зробити наступні вибірки з отриманої бази даних:

1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
2. Знайти студента із найвищим середнім балом з певного предмета.
3. Знайти середній бал у групах з певного предмета.
Знайти середній бал на потоці (по всій таблиці оцінок).
Знайти які курси читає певний викладач.
Знайти список студентів у певній групі.
Знайти оцінки студентів у окремій групі з певного предмета.
Знайти середній бал, який ставить певний викладач зі своїх предметів.
Знайти список курсів, які відвідує певний студент.
Список курсів, які певному студенту читає певний викладач.
"""


# Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():
    session = Session(engine)

    top_5_students = (
        session.query(Student.id, Student.name, func.avg(Grade.mark).label("avg_mark"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("avg_mark"))
        .limit(5)
        .all()
    )

    session.close()

    for student in top_5_students:
        print(
            f"ID: {student.id}, Name: {student.name}, Avg Mark: {student.avg_mark:.2f}"
        )


# Знайти студента із найвищим середнім балом з певного предмета.
def select_2(subject_name: str):
    session = Session(engine)

    top_student = (
        session.query(Student.id, Student.name, func.avg(Grade.mark).label("avg_mark"))
        .join(Grade)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(desc("avg_mark"))
        .limit(1)
        .first()
    )

    session.close()

    if top_student:
        print(
            f"Subject: {subject_name}, Student ID: {top_student.id}, Name: {top_student.name}, Avg Mark: {top_student.avg_mark:.2f}"
        )
    else:
        print(f"No grades found for subject: {subject_name}")


# Знайти середній бал у групах з певного предмета.
def select_3(subject_name: str):
    session = Session(engine)

    avg_grades = (
        session.query(
            Group.name.label("group_name"), func.avg(Grade.mark).label("avg_mark")
        )
        .select_from(Group)
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Subject.name == subject_name)
        .group_by(Group.name)
        .all()
    )

    session.close()

    if avg_grades:
        print(f"Subject: {subject_name}")

        for group in avg_grades:
            print(f"Group: {group.group_name}, Avg Mark: {group.avg_mark:.2f}")
    else:
        print(f"No data found for subject: {subject_name}")


# Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    session = Session(engine)

    avg_mark = session.query(func.avg(Grade.mark)).scalar()

    session.close()

    if avg_mark is not None:
        print(f"Average mark across all grades: {avg_mark:.2f}")
    else:
        print("No grades available.")


# Знайти які курси читає певний викладач.
def select_teacher():
    session = Session(engine)

    # Отримуємо список усіх викладачів
    teachers = session.query(Teacher.id, Teacher.name).all()
    session.close()

    if not teachers:
        print("No teachers found in the database.")
        return None

    print("List of teachers:")
    for teacher in teachers:
        print(f"{teacher.id}: {teacher.name}")

    while True:
        try:
            teacher_id = int(input("Enter the teacher's ID: "))
            teacher = next((t for t in teachers if t.id == teacher_id), None)
            if teacher:
                return teacher
            else:
                print("Invalid ID. Please enter a valid teacher ID from the list.")
        except ValueError:
            print("Invalid input. Please enter a numerical ID.")


def select_5(teacher: Teacher):
    session = Session(engine)

    courses = (
        session.query(Subject.name).join(Teacher).filter(Teacher.id == teacher.id).all()
    )

    session.close()

    if courses:
        print(f"Courses taught by {teacher.name}:")
        for course in courses:
            print(f"- {course.name}")
    else:
        print(f"No courses found for teacher: {teacher.name}")


# Знайти список студентів у певній групі.
def select_6(group_name: str):
    session = Session(engine)

    group = session.query(Group).filter(Group.name == group_name).first()

    if group:
        print(f"{group_name} student list:")
        students_in_group = (
            session.query(Student).filter(Student.group_id == group.id).all()
        )

        if students_in_group:
            for student in students_in_group:
                print(f"ID: {student.id}, Name: {student.name}")
    else:
        print("Group not found.")

    session.close()


# Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(group_name: str, subject_name: str):
    session = Session(engine)

    group = session.query(Group).filter(Group.name == group_name).first()

    if group:
        subject = session.query(Subject).filter(Subject.name == subject_name).first()

        if subject:
            grades = (
                session.query(Grade)
                .join(Student)
                .join(Subject)
                .filter(Student.group_id == group.id, Subject.id == subject.id)
                .all()
            )

            print(f"Subject {subject_name}, Group {group_name}")

            if grades:
                for grade in grades:
                    print(
                        f"Student: {grade.student.name}, Mark: {grade.mark}, Date: {grade.date_received}"
                    )

        else:
            print("Subject not found.")
    else:
        print("Group not found.")

    session.close()


# Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(teacher_id: str):
    session = Session(engine)

    results = (
        session.query(
            Subject.name.label("subject_name"),
            func.avg(Grade.mark).label("average_grade"),
        )
        .join(Grade)
        .filter(Subject.teacher_id == teacher_id)
        .group_by(Subject.id)
        .all()
    )

    if results:
        for subject, average in results:
            print(f"Subject: {subject}, Average grade: {average}")
    else:
        print("Teacher has not subjects.")

    session.close()


# Знайти список курсів, які відвідує певний студент.
def select_student():
    session = Session(engine)

    # Отримуємо список усіх cтудентів
    students = session.query(Student.id, Student.name).all()
    session.close()

    if not students:
        print("No students found in the database.")
        return None

    print("List of students:")
    for student in students:
        print(f"{student.id}: {student.name}")

    while True:
        try:
            student_id = int(input("Enter the student's ID: "))
            student = next((t for t in students if t.id == student_id), None)
            if student:
                return student
            else:
                print("Invalid ID. Please enter a valid student ID from the list.")
        except ValueError:
            print("Invalid input. Please enter a numerical ID.")


def select_9(student: Student):
    session = Session(engine)

    results = (
        session.query(Subject.name)
        .distinct()
        .join(Grade)
        .filter(Grade.student_id == student.id)
        .all()
    )

    if results:
        print(f"{student.name} courses:")

        for subject in results:
            print(f"- {subject.name}")
    else:
        print(f"Student {student.name} is not enrolled in any courses.")

    session.close()


# Список курсів, які певному студенту читає певний викладач.
def select_10(student: Student, teacher: Teacher):
    session = Session(engine)

    results = (
        session.query(Subject.name)
        .distinct()
        .join(Grade)
        .join(Teacher)
        .filter(Grade.student_id == student.id, Subject.teacher_id == teacher.id)
        .all()
    )

    if results:
        print(
            f"This teacher {teacher.name} teach this student {student.name} such courses:"
        )

        for subject in results:
            print(f"- {subject.name}")
    else:
        print(
            f"This teacher {teacher.name} does not teach any courses to this student {student.name}."
        )

    session.close()


if __name__ == "__main__":
    print("1 ***********************************************")

    select_1()

    print("2 ***********************************************")

    subject_name = SUBJECT_NAMES[1]
    select_2(subject_name)

    print("3 ***********************************************")

    select_3(subject_name)

    print("4 ***********************************************")

    select_4()

    print("5 ***********************************************")

    teacher = select_teacher()
    select_5(teacher)

    print("6 ***********************************************")

    group_name = GROUP_NAMES[0]
    select_6(group_name)

    print("7 ***********************************************")

    select_7(group_name, subject_name)

    print("8 ***********************************************")

    teacher = select_teacher()
    print(f"Teacher Name: {teacher.name}")
    select_8(teacher.id)

    print("9 ***********************************************")

    student = select_student()
    select_9(student)

    print("10 ***********************************************")

    teacher = select_teacher()
    student = select_student()
    select_10(student, teacher)
