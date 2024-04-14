from flask import Flask, jsonify
from .data_visualization.visualisations import visualization_blueprint
from .database import db
from .serializer import ma
from .views.student import student_blueprint
from .views.address import address_blueprint
from .data_cleaning import clean_data
from datetime import timedelta
from .data_loader import upload_data_to_database
from .init_jwt import jwt
from .views.auth_views_student import auth_blueprint



def create_app():
    """Flask System"""
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:admin@localhost/student_system"
    app.config["JWT_SECRET_KEY"] = "istanbul"
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)


    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()
        db.session.commit()
        upload_data_to_database("student-dataset.csv")



    app.register_blueprint(address_blueprint)
    app.register_blueprint(student_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(visualization_blueprint)



    @app.route('/api/cleaned_data')
    def get_cleaned_data():
        # Load and clean the dataset
        cleaned_dataset = clean_data("student-dataset.csv")

        # Convert DataFrame to JSON
        cleaned_data_json = cleaned_dataset.to_dict(orient="records")

        # Return JSON response using Flask's jsonify function
        return jsonify(cleaned_data_json)


    return app

