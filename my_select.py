from sqlalchemy import func, desc, select, and_
from conf.models import Grade, Teacher, Student, Group, Subject
from conf.db import session




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

if __name__=="__main__":
    print(select_08(18))
