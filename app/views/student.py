from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.database import db
from app.models.student import Student
from app.schemas.student_schema import StudentSchema

student_blueprint = Blueprint("student", __name__)

@student_blueprint.route("/api/student", methods=["GET", "POST"])
@jwt_required()
def student_list():
    """Return all users from JSON Placeholder API"""
    if request.method == "GET":
        students = db.session.query(Student).all()
        if len(students) <= 0:
            error_msg = "No results."
            return jsonify(msg=error_msg, status=200), 200

        schema = StudentSchema(many=True)
        data = schema.dump(students)

        return jsonify(
            data=data,
            status=200
        ), 200
    # Get the JSON data from the request body.
    # Make sure to import 'request' from flask at the top.

    else:
        data = request.json
        # Try getting name, city, age, and  fields from our data, using dictionary indexing.

        try:
                name = data["name"]
                nationality = ["nationality"]
                city = data["city"]
                latitude = data["latitude"]
                longitude = data["longitude"]
                gender = data["gender"]
                age = data["age"]
                english_grade = data["english_grade"]
                math_grade = data["math_grade"]
                sciences_grade = data["sciences_grade"]
                language_grade = data["language_grade"]
                portfolio_rating = data["portfolio_rating"]
                coverletter_rating = data["coverletter_rating"]
                refletter_rating = data["refletter_rating"]

                # Create a new instance of Student, passing in the required fields.
                new_student = Student(name=name, nationality= nationality, city=city, latitude=latitude, longitude = longitude, gender=gender, age=age, english_grade=english_grade, math_grade=math_grade, sciences_grade=sciences_grade, language_grade=language_grade, portfolio_rating=portfolio_rating, coverletter_rating=coverletter_rating, refletter_rating=refletter_rating)
                # Add the new user to the database.
                db.session.add(new_student)
                # Commit the transaction. This is required to actually save the new student.
                db.session.commit()

                success_msg = "New student created."
                # Return a success message, the same data that was sent in the request, and a 201 (Created) response status.
                return jsonify(data=data, msg=success_msg, status=201), 201
        # If there is a KeyError, this means that either 'name', 'age', 'gender' are not present
        # in the request data.
        except KeyError:
            error_msg = "Please specify all required fields."
            return jsonify(msg=error_msg, status=400), 400

@student_blueprint.route("/api/student/<int:student_id>", methods=["GET"])
@jwt_required()
def get_single_student(student_id):

    """Return a single user from JSON Placeholder API."""
    student = db.session.query(Student).filter_by(id=student_id).first()
    if not student:
        error_msg = "Student not found. Try a different ID."
        return jsonify(msg=error_msg, status=200), 200

    schema = StudentSchema(many=False)
    data = schema.dump(student)
    return jsonify(data=data, status=200), 200

@student_blueprint.route("/api/student/<int:student_id>", methods=["PATCH"])
@jwt_required()
def student_partial_update(student_id):
    """Perform partial update of user."""
    data = request.json

    student = db.session.query(Student).filter_by(id=student_id).first()
    if not student:
        error_msg = "Student does not exist. Try a different ID."
        return jsonify(msg=error_msg, status=400), 400

    try:
        for key, value in data.items():
            if not hasattr(student, key):
                raise ValueError
            else:
                setattr(student, key, value)
                db.session.commit()

        updated_student = db.session.query(Student).filter_by(id=student_id).first()

        schema = StudentSchema(many=False)
        data = schema.dump(updated_student)

        return jsonify(data=data, status=200), 200

    except ValueError:
        error_msg = "Error referencing columns with provided keys."
        return jsonify(msg=error_msg, status=400), 400

@student_blueprint.route("/api/student/<int:student_id>", methods=["DELETE"])
@jwt_required()
def delete_student(student_id):
    """Perform DELETE request to delete user."""
    student = db.session.query(Student).filter_by(id=student_id).first()
    msg = None
    if not student:
        msg = "Student not found."
    else:
        db.session.delete(student)
        db.session.commit()
        msg = f"Student with id {student_id} deleted."
    return msg, 200
