# Import necessary libraries
from flask import Flask, jsonify, Blueprint, send_file
from flask_jwt_extended import jwt_required
import pandas as pd
import matplotlib.pyplot as plt
import io

# Create Flask app
app = Flask(__name__)

# Define a blueprint for visualizations
visualization_blueprint = Blueprint('visualization_blueprint', __name__)

# Load the student dataset into a DataFrame
df = pd.read_csv("student-dataset.csv")

# Analysis 1: Count the number of students with the highest math grade
highest_math_grade = df["math.grade"].max()
num_students_highest_math_grade = df[df["math.grade"] == highest_math_grade].shape[0]

# Analysis 2: Count the number of students with the highest English grade
highest_english_grade = df["english.grade"].max()
num_students_highest_english_grade = df[df["english.grade"] == highest_english_grade].shape[0]

# Analysis 3: Count the number of students from each country
country_counts = df["nationality"].value_counts()

# Analysis 4: Compare science grades between genders
science_grades_by_gender = df.groupby("gender")["sciences.grade"].mean()

# Create visualizations
# Visualization 1: Bar chart for country distribution
plt.figure(figsize=(10, 6))
country_counts.plot(kind="bar", color="skyblue")
plt.title("Number of Students from Each Country")
plt.xlabel("Country")
plt.ylabel("Number of Students")
plt.xticks(rotation=45)
plt.tight_layout()
country_distribution_buffer = io.BytesIO()
plt.savefig(country_distribution_buffer, format='png')
plt.close()

# Visualization 2: Bar chart for science grades by gender
plt.figure(figsize=(8, 5))
science_grades_by_gender.plot(kind="bar", color=["lightblue", "lightpink"])
plt.title("Average Science Grade by Gender")
plt.xlabel("Gender")
plt.ylabel("Average Science Grade")
plt.xticks(rotation=0)
plt.tight_layout()
science_grade_by_gender_buffer = io.BytesIO()
plt.savefig(science_grade_by_gender_buffer, format='png')
plt.close()

# Define endpoints
@visualization_blueprint.route("/api/visualizations/country_distribution")
@jwt_required()
def get_country_distribution_viz():
    country_distribution_buffer.seek(0)
    return send_file(country_distribution_buffer, mimetype='image/png')

@visualization_blueprint.route("/api/visualizations/science_grade_by_gender")
@jwt_required()
def get_science_grade_by_gender_viz():
    science_grade_by_gender_buffer.seek(0)
    return send_file(science_grade_by_gender_buffer, mimetype='image/png')

# Register blueprint
app.register_blueprint(visualization_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
# Output analysis results to files
country_counts.to_csv("country_counts.csv", header=True)
science_grades_by_gender.to_csv("science_grades_by_gender.csv", header=True)


