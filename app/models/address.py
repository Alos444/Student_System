

from app.database import db

class Address(db.Model):
    """Model to represent a student record in the database."""

    __tablename__ = "address"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    house_name = db.Column(db.String(50), nullable=False)
    road = db.Column(db.String(15), nullable= False)
    city = db.Column(db.String(15), nullable= False)
    state = db.Column(db.String(15), nullable=True)
    country = db.Column(db.String(15), nullable=False)
    zipcode = db.Column(db.String(15), nullable=True)
    student = db.relationship("Student", back_populates="address")

    def __init__(self, student_id, number, house_name, road, city, state, country, zipcode):
        self.student_id = student_id
        self.number = number
        self.house_name = house_name
        self.road = road
        self.city = city
        self.state = state
        self.country = country
        self.zipcode = zipcode

    def __repr__(self):
        return f"Record for Address {self.student_id}: house_name {self.house_name}, road {self.road}, city {self.city}, state {self.state}, country{self.country}, zipcode {self.zipcode},  "
