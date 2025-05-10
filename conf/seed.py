import random
from faker import Faker

from db import DBSession
from models import Teacher, Group, Student, Subject, Grade

fake = Faker()
session = DBSession()

NUM_STUDENTS = 50
NUM_GROUPS = 3
NUM_TEACHERS = 5
NUM_SUBJECTS = 8
MAX_GRADES_PER_STUDENT = 20


try:
    # Pre-cleanup in case there is already data
    session.query(Grade).delete()
    session.query(Student).delete()
    session.query(Subject).delete()
    session.query(Teacher).delete()
    session.query(Group).delete()
    session.commit()

    # Create grupos
    groups = [Group(name=fake.word()) for _ in range(NUM_GROUPS)]
    session.add_all(groups)
    session.commit()

    # Create teachers
    teachers = [Teacher(fullname=fake.name()) for _ in range(NUM_TEACHERS)]
    session.add_all(teachers)
    session.commit()

    # Create subject
    subjects = [Subject(name=fake.catch_phrase(), teacher=random.choice(teachers)) for _ in range(NUM_SUBJECTS)]
    session.add_all(subjects)
    session.commit()

    # Create students
    students = [Student(fullname=fake.name(), group=random.choice(groups)) for _ in range(NUM_STUDENTS)]
    session.add_all(students)
    session.commit()

    # Create grades
    grades = []
    for student in students:
        for _ in range(random.randint(10, MAX_GRADES_PER_STUDENT)):
            grade = Grade(
                student=student,
                subject=random.choice(subjects),
                grade=random.randint(60, 100),
                grade_date=fake.date_between(start_date="-6m", end_date="today")
            )
            grades.append(grade)
    session.add_all(grades)
    session.commit()

    print("✅ Database populated successfully.")

except Exception as e:
    session.rollback()
    print(f"❌ Error: {e}")

finally:
    session.close()