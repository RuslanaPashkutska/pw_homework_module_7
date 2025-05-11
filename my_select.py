from sqlalchemy import func, desc, select, and_
from conf.models import Grade, Teacher, Student, Group, Subject
from conf.db import session
import argparse



def select_01():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN grades g ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 5;
    """

    result = session.query(
        Student.id,
        Student.fullname,
        func.round(func.avg(Grade.grade), 2).label("average_grade")) \
        .join(Grade).group_by(Student.id).order_by(desc("average_grade")).limit(5).all()
    return result


def select_02(subject_id):
    result = session.query(
        Student.fullname,
        func.round(func.avg(Grade.grade), 2).label("average_grade")
    ) \
    .join(Grade) \
    .filter(Grade.subject_id == subject_id) \
    .group_by(Student.id) \
    .order_by(desc("average_grade")) \
    .limit(1) \
    .all()
    return result

def select_03(subject_id):
    result = (session.query(
        Group.name,
        func.round(func.avg(Grade.grade), 2).label("average_grade")
    ) \
    .select_from(Group)
    .join(Student) \
    .join(Grade) \
    .filter(Grade.subject_id == subject_id) \
    .group_by(Group.name) \
    .order_by(Group.name) \
    .all())

    return result

def select_04():
    result = session.query(
        func.round(func.avg(Grade.grade), 2).label("average_grade")).scalar()
    return result

def select_05(teacher_id):
    result = session.query(Subject.name) \
        .join(Teacher) \
        .filter(Subject.teacher_id == teacher_id) \
        .all()
    return result

def select_06(group_id):
    result = session.query(Student.fullname) \
        .filter(Student.group_id == group_id) \
        .all()
    return result

def select_07(group_id, subject_id):
    result = session.query(
        Student.fullname,
        Grade.grade,
        Grade.grade_date
    ) \
    .join(Group) \
    .join(Grade) \
    .filter(Group.id == group_id) \
    .filter(Grade.subject_id == subject_id) \
    .all()
    return result


def select_08(teacher_id):
    result = session.query(
        func.round(func.avg(Grade.grade), 2).label("average_grade")
    ) \
    .join(Subject) \
    .join(Teacher) \
    .filter(Teacher.id == teacher_id) \
    .all()
    return result

def select_09(student_id):
    result = session.query(Subject.name) \
        .join(Grade, Subject.id == Grade.subject_id) \
        .filter(Grade.student_id == student_id) \
        .all()
    return result

def select_10(student_id, teacher_id):
    result = session.query(Subject.name) \
        .join(Grade, Grade.subject_id == Subject.id) \
        .join(Teacher, Teacher.id == Subject.teacher_id) \
        .filter(Grade.student_id == student_id) \
        .filter(Teacher.id == teacher_id) \
        .all()
    return result

# SECOND PART OF THE TASK

def select_11(student_id, teacher_id):
    result = session.query(
        func.round(func.avg(Grade.grade), 2).label("average_grade")
    ) \
    .join(Subject, Grade.subject_id == Subject.id) \
    .join(Teacher, Subject.teacher_id == Teacher.id) \
    .filter(Teacher.id == teacher_id) \
    .filter(Grade.student_id == student_id) \
    .scalar()
    return result


def select_12(group_id, subject_id):
    last_date = session.query(func.max(Grade.grade_date)) \
        .join(Student) \
        .filter(Student.group_id == group_id) \
        .filter(Grade.subject_id == subject_id) \
        .scalar()

    result = session.query(
        Student.fullname,
        Grade.grade,
        Grade.grade_date
    ) \
    .join(Grade) \
    .filter(Student.group_id == group_id) \
    .filter(Grade.subject_id == subject_id) \
    .filter(Grade.grade_date == last_date) \
    .all()

    return result

#THIRD PART OF THE TASK
#Groups
def create_group(name):
    group = Group(name=name)
    session.add(group)
    session.commit()
    print(f"Created Group: {group}")

def list_groups():
    groups = session.query(Group).all()
    for g in groups:
        print(f"{g.id}: {g.name}")

def update_group(group_id, name):
    group = session.get(Group, group_id)
    if group:
        group.name = name
        session.commit()
        print(f"Update Group: {group}")
    else:
        print("Group not found.")

def remove_group(group_id):
    group = session.get(Group, group_id)
    if group:
        session.delete(group)
        session.commit()
        print(f"Removed Group: {group}")
    else:
        print("Group not found.")

#Teachers
def create_teacher(name):
    teacher = Teacher(name=name)
    session.add(teacher)
    session.commit()
    print(f"Created Teacher: {teacher}")

def list_teachers():
    teachers = session.query(Teacher).all()
    for t in teachers:
        print(f"{t.id}: {t.name}")

def update_teacher(teacher_id, name):
    teacher = session.get(Teacher, teacher_id)
    if teacher:
        teacher.name = name
        session.commit()
        print(f"Update Teacher: {teacher}")
    else:
        print("Teacher not found.")

def remove_teacher(teacher_id):
    teacher = session.get(Teacher, teacher_id)
    if teacher:
        session.delete(teacher)
        session.commit()
        print(f"Removed Teacher: {teacher}")
    else:
        print("Teacher not found.")



#Subject
def create_subject(name, teacher_id):
    subject = Subject(name=name, teacher_id=teacher_id)
    session.add(subject)
    session.commit()
    print(f"Created Subject: {subject}")

def list_subjects():
    subjects = session.query(Subject).all()
    for s in subjects:
        print(f"{s.id}: {s.name} (Teacher ID: {s.teacher_id})")

def update_subject(subject_id, name):
    subject = session.get(Subject, subject_id)
    if subject:
        subject.name = name
        session.commit()
        print(f"Update Subject: {subject}")
    else:
        print("Subject not found.")

def remove_subject(subject_id):
    subject = session.get(Subject, subject_id)
    if subject:
        session.delete(subject)
        session.commit()
        print(f"Removed Subject: {subject}")
    else:
        print("Subject not found.")


#Student
def create_student(name, group_id):
    student = Student(fullname=name, group_id=group_id)
    session.add(student)
    session.commit()
    print(f"Created Student: {student}")

def list_students():
    students = session.query(Student).all()
    for s in students:
        print(f"{s.id}: {s.fullname} (Group ID: {s.group_id})")

def update_student(student_id, name):
    student = session.get(Student, student_id)
    if student:
        student.fullname = name
        session.commit()
        print(f"Update Student: {student}")
    else:
        print("Student not found.")

def remove_student(student_id):
    student = session.get(Student, student_id)
    if student:
        session.delete(student)
        session.commit()
        print(f"Removed Student: {student}")
    else:
        print("Student not found.")



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", choices=["create", "list", "update", "remove"], required=True)
    parser.add_argument("-m", "--model", choices=["Group", "Teacher", "Subject", "Student"], required=True)
    parser.add_argument("-n", "--name", help="Name of the object")
    parser.add_argument("--id", type=int, help="ID of the group")
    parser.add_argument("--teacher_id", type=int, help="Teacher ID")
    parser.add_argument("--group_id", type=int, help="Group ID")
    args = parser.parse_args()

    if args.model == "Group":
        if args.action == "create" and args.name:
            create_group(args.name)
        elif args.action == "list":
            list_groups()
        elif args.action == "update" and args.id and args.name:
            update_group(args.id, args.name)
        elif args.action == "remove" and args.id:
            remove_group(args.id)
        else:
            print("Invalid arguments for Group model.")


    elif args.model == "Teacher":
        if args.action == "create" and args.name:
            create_teacher(args.name)
        elif args.action == "list":
            list_teachers()
        elif args.action == "update" and args.id and args.name:
            update_teacher(args.id, args.name)
        elif args.action == "remove" and args.id:
            remove_teacher(args.id)
        else:
            print("Invalid arguments for Teacher model.")

    elif args.model == "Subject":
        if args.action == "create" and args.name and args.teacher_id:
            create_subject(args.name, args.teacher_id)
        elif args.action == "list":
            list_subjects()
        elif args.action == "update" and args.id and args.name:
            update_subject(args.id, args.name)
        elif args.action == "remove" and args.id:
            remove_subject(args.id)
        else:
            print("Invalid arguments for Subject model.")

    elif args.model == "Student":
        if args.action == "create" and args.name and args.group_id:
            create_student(args.name, args.group_id)
        elif args.action == "list":
            list_students()
        elif args.action == "update" and args.id and args.name:
            update_student(args.id, args.name)
        elif args.action == "remove" and args.id:
            remove_student(args.id)
        else:
            print("Invalid arguments for Student model.")