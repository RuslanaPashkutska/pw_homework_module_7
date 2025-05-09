import logging
import random
from faker import Faker
import psycopg2
from psycopg2 import DatabaseError

logging.basicConfig(level=logging.INFO)
fake = Faker()

NUM_STUDENTS = 40
NUM_GROUPS = 3
NUM_TEACHERS = 5
NUM_SUBJECTS = 7
MAX_GRADES_PER_STUDENT = 20


conn = None
cur = None

logging.info("Connect to the database...")
try:
    conn = psycopg2.connect(
        host="localhost",
        database="module_7",
        user="example",
        password="example"
    )
    cur = conn.cursor()


    # Delete existing data
    cur.execute("DELETE FROM grades")
    cur.execute("DELETE FROM students")
    cur.execute("DELETE FROM subjects")
    cur.execute("DELETE FROM teachers")
    cur.execute("DELETE FROM groups")
    conn.commit()

    # Insert groups
    group_ids = []
    for _ in range(NUM_GROUPS):
        cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (fake.word(),))
        group_ids.append(cur.fetchone()[0])

    # Insert teachers
    teacher_ids = []
    for _ in range(NUM_TEACHERS):
        cur.execute("INSERT INTO teachers (fullname) VALUES (%s) RETURNING id", (fake.name(),))
        teacher_ids.append(cur.fetchone()[0])

    # Insert subjects
    subject_ids = []
    for _ in range(NUM_SUBJECTS):
        cur.execute("INSERT INTO subjects (name, teacher_id) VALUES (%s, %s) RETURNING id",
                    (fake.catch_phrase(), random.choice(teacher_ids)))
        subject_ids.append(cur.fetchone()[0])


    # Insert students
    student_ids = []
    for _ in range(NUM_STUDENTS):
        cur.execute("INSERT INTO students (fullname, group_id) VALUES (%s, %s) RETURNING id",
                    (fake.name(), random.choice(group_ids)))
        student_ids.append(cur.fetchone()[0])


    # Insert grades
    for student_id in student_ids:
        for _ in range(random.randint(10, MAX_GRADES_PER_STUDENT)):
            cur.execute(
                "INSERT INTO grades (student_id, subject_id, grade, grade_date) VALUES (%s, %s, %s, %s)",
                (
                    student_id,
                    random.choice(subject_ids),
                    random.randint(60, 100),
                    fake.date_between(start_date="-6m", end_date="today")
                )
            )


    conn.commit()
    logging.info("Data successfully generated and saved in the database.")
    logging.info(f"Total groups: {len(group_ids)}, teachers: {len(teacher_ids)}, subjects: {len(subject_ids)}, students: {len(student_ids)}")


except DatabaseError as e:
    logging.exception("Database error:")
    if conn:
        conn.rollback()

except Exception  as e:
    logging.error(f"Exception Error: {e}")
    if conn:
        conn.rollback()

finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()