

from app.serializer import ma
from app.models.student import Student
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.schemas.address_schema import AddressSchema


class StudentSchema(SQLAlchemyAutoSchema):
    """Serializable schema for the Student SQLAlchemy object."""

    class Meta:
        # Provide the Student model to serialize.
        model = Student

        # Define the fields which will be in the output when Student model is serialized.
        fields = ("id", "name", "nationality", "city", "latitude", "longitude", "gender", "age",
                  "english_grade", "math_grade", "sciences_grade", "language_grade", "portfolio_rating",
                  "coverletter_rating", "refletter_rating", "records")

    addresses = ma.Nested(AddressSchema, many=True)

