

from flask import Flask, jsonify, request
import pandas as pd



app = Flask(__name__)

# Load the student dataset
df = pd.read_csv("student-dataset.csv")



# Perform the analysis
highest_math_grade = df["math.grade"].max()
num_students_highest_math_grade = df[df["math.grade"] == highest_math_grade].shape[0]

highest_english_grade = df["english.grade"].max()
num_students_highest_english_grade = df[df["english.grade"] == highest_english_grade].shape[0]

country_distribution = df["nationality"].value_counts().to_dict()

science_grades_by_gender = df.groupby("gender")["sciences.grade"].mean().to_dict()

# Define endpoints
@app.route("/api/highest_math_grade", methods=["GET"])
def get_highest_math_grade():
    if request.method == "GET":
        return jsonify({"num_students_highest_math_grade": num_students_highest_math_grade})

@app.route("/api/highest_english_grade", methods=["GET"])
def get_highest_english_grade():
    if request.method == "GET":
        return jsonify({"num_students_highest_english_grade": num_students_highest_english_grade})

@app.route("/api/country_distribution", methods=["GET"])
def get_country_distribution(country_distribution):
    if request.method == "GET":
        return jsonify({"country_distribution": country_distribution})

@app.route("/api/science_grade_by_gender", methods=["GET"])
def get_science_grade_by_gender(science_grade_by_gender):
    if request.method == "GET":
        return jsonify({"science_grades_by_gender": science_grades_by_gender})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
