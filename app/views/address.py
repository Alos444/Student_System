from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.database import db
from app.models.address import Address
from app.models.student import Student
from app.schemas.address_schema import AddressSchema

address_blueprint = Blueprint("address", __name__)

@address_blueprint.route("/api/address", methods=["GET", "POST"])
@jwt_required()
def address_list():
    """Return all users from JSON Placeholder API"""
    if request.method == "GET":
        addresses = db.session.query(Address).all()
        if len(addresses) <= 0:
            error_msg = "No results."
            return jsonify(msg=error_msg, status=200), 200
        # Replace with schema dump and return JSON.
        schema = AddressSchema(many=True)
        data = schema.dump(addresses)

        return jsonify(
            data=data,
            status=200
        ), 200

    else:
        data = request.json

        try:
            student_id = data["student_id"]
            student = db.session.query(Student).filter_by(id=student_id).first()
            # .first() returns an object
            # .all() returns a list of objects. This is iterable.
            if not student:
                error_msg = "Student  not found. Please try a different id."
                return jsonify(msg=error_msg, status=400), 400
            number = data["number"]
            house_name = data["house_name"]
            road = data["road"]
            city = data["city"]
            state = data["state"]
            country = data["country"]
            zipcode = data["zipcode"]

            new_address = Address(student_id=student_id, number=number, house_name=house_name, road=road, city=city, state=state, country=country, zipcode=zipcode)
            db.session.add(new_address)
            db.session.commit()

            success_msg = "New record created."
            return jsonify(data=data, msg=success_msg, status=201), 201

        except KeyError:
            error_msg = "Please specify ,<student_id> and all necessary fields."
            return jsonify(msg=error_msg, status=400), 400

@address_blueprint.route("/api/address/<int:student_id>", methods=["GET"])
@jwt_required()
def get_single_address(student_id):
    address = db.session.query(Address).filter_by(id=student_id).first()
    if not address:
        error_msg = "Record not found. Try a different ID."
        return jsonify(msg=error_msg, status=200), 200
    #  Replace with schema dump and return as JSON.
    schema = AddressSchema(many=False)
    data = schema.dump(address)
    return jsonify(data=data, status=200), 200

@address_blueprint.route("/api/address/<int:student_id>", methods=["PATCH"])
@jwt_required()
def address_partial_update(student_id):
    """Perform partial update of post."""
    data = request.json

    address = db.session.query(Address).filter_by(id=student_id).first()
    if not address:
        error_msg = "Record does not exist. Try a different ID."
        return jsonify(msg=error_msg, status=400), 400

    try:
        for key, value in data.items():
            if not hasattr(address, key):
                raise ValueError
            else:
                setattr(address, key, value)
                db.session.commit()

        updated_address = db.session.query(Address).filter_by(id=student_id).first()

        schema = AddressSchema(many=False)
        data = schema.dump(updated_address)

        return jsonify(data=data, status=200)

    except ValueError:
        error_msg = "Error referencing columns with provided keys."
        return jsonify(msg=error_msg, status=400), 400

@address_blueprint.route("/api/address/<int:student_id>", methods=["DELETE"])
@jwt_required()
def delete_address(student_id):
    """Perform DELETE request to delete address."""
    address = db.session.query(Address).filter_by(id=student_id).first()
    msg = None
    if not address:
        msg = "Record not found."
    else:
        db.session.delete(address)
        db.session.commit()
        msg = f"Record with id {student_id} deleted."
    return msg, 200
