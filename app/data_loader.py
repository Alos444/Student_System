import pandas as pd
from app.models.student import Student
from app.database import db

def upload_data_to_database(file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file)

    # Iterate over the rows of the DataFrame
    for _, row in df.iterrows():
        # Create a new Student object and populate its attributes with data from the DataFrame row
        student = Student(
            name=row['name'],
            nationality=row['nationality'],
            city=row['city'],
            latitude=row['latitude'],
            longitude=row['longitude'],
            gender=row['gender'],
            age=row['age'],
            english_grade=row['english.grade'],
            math_grade=row['math.grade'],
            sciences_grade=row['sciences.grade'],
            language_grade=row['language.grade'],
            portfolio_rating=row['portfolio.rating'],
            coverletter_rating=row['coverletter.rating'],
            refletter_rating=row['refletter.rating']
        )

        # Add the new student to the database session
        db.session.add(student)

    # Commit the transaction to save all changes to the database
    db.session.commit()

# Usage example
if __name__ == "__main__":
    upload_data_to_database("student-dataset.csv")
