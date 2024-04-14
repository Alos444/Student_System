from app.database import db
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import OperationalError, IntegrityError

import time


class AuthStudent(db.Model):
    """Model to represent an Auth Student in the DB."""

    __tablename__ = "auth_student"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    def get_student(self, password):
        """Return auth student from database"""

        try:
            student = AuthStudent.query.filter_by(email=self.email).first()
            if student:
                if check_password_hash(student.password, password):
                    return student
                else:
                    return "wrong password"
            else:
                return "not found"
        except Exception as e:
            print(f"Exception: {e}")
            return None

    def create_jwt_token(self):
        return create_access_token(self.email)

    @staticmethod
    def refresh_jwt_token(func):
        return create_access_token(identity=func())

    def add_student(self):

        num_retries = 5
        student_registration_success = False

        while num_retries > 0:
            try:
                db.session.add(self)
                db.session.commit()
                student_registration_success = True
                break
            except OperationalError:
                num_retries -= 1  # num_retries = num_retries - 1
                time.sleep(1)
            except IntegrityError:
                db.session.rollback()
                return False

        if not student_registration_success:
            return None
        else:
            return True
