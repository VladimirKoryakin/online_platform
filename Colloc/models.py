import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import host, user, password, db_name, port
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    lecturer = Column(String(255))
    name = Column(String(255))
    price = Column(Integer)
    description = Column(String(1000))
    program = Column(String(1000))
    reviews = Column(JSONB)

    def __init__(self, lecturer, name, price, description, program, reviews=None):
        self.name = name
        self.lecturer = lecturer
        self.price = price
        self.description = description
        self.program = program
        self.reviews = reviews

    def __repr__(self):
        return f"({self.id}) {self.name}"


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255))
    last_name = Column(String(255))

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class Enrollment(Base):
    __tablename__ = 'enrollments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    student_id = Column(Integer, ForeignKey('students.id'))

    def __init__(self, course_id, student_id):
        self.course_id = course_id
        self.student_id = student_id


if __name__ == '__main__':
    url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    engine = create_engine(url, pool_size=50, echo=True)
    print(engine.url)
    session = sessionmaker(bind=engine)()
    print(session)
    Base.metadata.create_all(engine)
    session.commit()
    courses = [Course('Green', 'Java', 100, 'Very cool course!', "You'll learn how to code!"),
               Course('Red', 'Python', 300, 'Very easy course!', "You'll learn how to code!"),
               Course('Blue', 'C++', 2000, 'Very sad course!', "You'll learn how to code!",
                      {1: {"student_id": 1, "text": "Won't recommend it to anyone("}})]
    for course in courses:
        session.add(course)
    session.commit()
    students = [Student('Mick', 'Jagger'),
                Student('Paul', 'McCartney'),
                Student('John', 'Lennon')]
    for student in students:
        session.add(student)
    session.commit()
    enrollments = [Enrollment(3, 1), Enrollment(1, 1), Enrollment(2, 3), Enrollment(2, 2), Enrollment(1, 3)]
    for enrollment in enrollments:
        session.add(enrollment)
    session.commit()
