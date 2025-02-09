from sqlalchemy import ForeignKey, Column, Integer, String, Float, Date, PrimaryKeyConstraint, func
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from datetime import datetime
from connectdb import Base

class Group(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    students: Mapped[list['Student']] = relationship('Student', back_populates='group')


class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(250), unique=True)

    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'), nullable=False)
    group: Mapped['Group'] = relationship('Group', back_populates='students')

    grades: Mapped[list['Grade']] = relationship('Grade', back_populates='student')


class Teacher(Base):
    __tablename__ = 'teachers'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)

    subjects: Mapped[list['Subject']] = relationship('Subject', back_populates='teacher')

class Subject(Base):
    __tablename__ = 'subjects'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)

    teacher_id: Mapped[int] = mapped_column(ForeignKey('teachers.id'))
    teacher: Mapped['Teacher'] = relationship('Teacher', back_populates='subjects')

    grades: Mapped[list['Grade']] = relationship('Grade', back_populates='subject')

class Grade(Base):
    __tablename__ = 'grades'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mark: Mapped[float] = mapped_column(Integer, nullable=False)
    date_received: Mapped[datetime] = mapped_column(Date, nullable=False)

    student_id: Mapped[int] = mapped_column(ForeignKey('students.id'))
    subject_id: Mapped[int] = mapped_column(ForeignKey('subjects.id'))
   
    student: Mapped['Student'] = relationship('Student', back_populates='grades')
    subject: Mapped['Subject'] = relationship('Subject', back_populates='grades')
