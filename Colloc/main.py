from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import host, user, password, db_name, port
from models import Course, Student, Enrollment


url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
engine = create_engine(url, pool_size=50, echo=False)
print(engine.url)
session = sessionmaker(bind=engine)()
print(session)

app = Flask(__name__)
api = Api()


@app.get('/courses')
def get_courses_info():
    courses = session.query(Course).all()
    answer = {}
    for course in courses:
        answer[course.id] = {"name": course.name,
                             "lecturer": course.lecturer,
                             "description": course.description,
                             "price": course.price}
    return answer


@app.get('/courses/<int:course_id>')
def get_course_info(course_id):
    try:
        course = session.query(Course).filter(Course.id == course_id).one()
    except Exception:
        return "Invalid course_id, there's no such course!", 400

    answer = {}
    answer[course.id] = {"name": course.name,
                         "lecturer": course.lecturer,
                         "description": course.description,
                         "price": course.price,
                         "program": course.program,
                         "reviews": course.reviews}
    return answer


@app.post('/enrollments')
def add_enrollment():
    try:
        data = request.get_json()
    except Exception as ex:
        return "Request should be in JSON format!", 406

    try:
        course_id = data['course_id']
        student_id = data['student_id']
    except Exception as ex:
        return "Incorrect input format, there should be couse_id and student_id in JSON!", 400
    enrollment = Enrollment(course_id, student_id)
    session.add(enrollment)
    session.commit()
    return "Enrollment is successfully added!", 200


@app.get('/enrollments/<int:student_id>')
def get_users_courses(student_id):
    enrollments = session.query(Enrollment).filter(Enrollment.student_id == student_id).all()

    answer = {}
    for enroll in enrollments:
        course = course = session.query(Course).filter(Course.id == enroll.course_id).one()
        answer[course.id] = {"name": course.name,
                            "lecturer": course.lecturer,
                            "description": course.description,
                            "price": course.price,
                            "program": course.program,
                            "reviews": course.reviews}
    return answer


@app.delete('/enrollments/<int:enrollment_id>')
def delete_enrollment(enrollment_id):
    try:
        enrollment = session.query(Enrollment).filter(Enrollment.id == enrollment_id).one()
    except Exception:
        return "Invalid enrollment_id!", 400

    session.delete(enrollment)
    session.commit()
    return f"Enrollment {enrollment_id} was deleted successfully!", 200


api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="127.0.0.1")
