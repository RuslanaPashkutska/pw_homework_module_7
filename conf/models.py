from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)
    subjects = relationship('Subject', back_populates='teacher')


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    students = relationship('Student', back_populates='group')


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)
    group_id = Column(ForeignKey('groups.id', ondelete='CASCADE'))
    group = relationship('Group', back_populates='students')
    grades = relationship('Grade', back_populates='student')


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(175), nullable=False)
    teacher_id = Column('teacher_id', ForeignKey('teachers.id', ondelete='CASCADE'))
    teacher = relationship('Teacher', back_populates='subjects')
    grades = relationship('Grade', back_populates='subject')


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    grade_date = Column('grade_date', Date, nullable=True)
    student_id = Column('student_id', ForeignKey('students.id', ondelete='CASCADE'))
    subject_id = Column(ForeignKey('subjects.id', ondelete='CASCADE'))
    student = relationship('Student', back_populates='grades')
    subject = relationship('Subject', back_populates='grades')