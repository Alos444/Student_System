from sample.student import Student
from sqlalchemy import ForeignKey

from app.database import db
from app.models.address import Address


class Student(db.Model):
    """Model to represent a student record in the database."""

    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    nationality = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    english_grade = db.Column(db.Float, nullable=False)
    math_grade = db.Column(db.Float, nullable=False)
    sciences_grade = db.Column(db.Float, nullable=False)
    language_grade = db.Column(db.Float, nullable=False)
    portfolio_rating = db.Column(db.Float, nullable=False)
    coverletter_rating = db.Column(db.Float, nullable=False)
    refletter_rating = db.Column(db.Float, nullable=False)

    # Define the relationship with Address model

    address = db.relationship("Address", back_populates="student")



    def __init__(self, name, nationality, city, latitude, longitude, gender, age,
                 english_grade, math_grade, sciences_grade, language_grade,
                 portfolio_rating, coverletter_rating, refletter_rating):
        self.name = name
        self.nationality = nationality
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.gender = gender
        self.age = age
        self.english_grade = english_grade
        self.math_grade = math_grade
        self.sciences_grade = sciences_grade
        self.language_grade = language_grade
        self.portfolio_rating = portfolio_rating
        self.coverletter_rating = coverletter_rating
        self.refletter_rating = refletter_rating


    def __repr__(self):
        return f"Student {self.id}: {self.name}"
