
from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

model = joblib.load("student_score_model.pkl")


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    error = None

    if request.method == "POST":
        try:
            study_hours = float(request.form["study_hours"])
            attendance = float(request.form["attendance"])
            previous_score = float(request.form["previous_score"])
            sleep_hours = float(request.form["sleep_hours"])

            if not 0 <= study_hours <= 24:
                raise ValueError("Study hours must be between 0 and 24.")
            if not 0 <= attendance <= 100:
                raise ValueError("Attendance must be between 0 and 100.")
            if not 0 <= previous_score <= 100:
                raise ValueError("Previous score must be between 0 and 100.")
            if not 0 <= sleep_hours <= 24:
                raise ValueError("Sleep hours must be between 0 and 24.")

            student = pd.DataFrame([{
                "study_hours_per_day": study_hours,
                "attendance_percent": attendance,
                "previous_exam_score": previous_score,
                "sleep_hours": sleep_hours
            }])

            prediction = round(float(model.predict(student)[0]), 1)
            prediction = max(0, min(100, prediction))

        except ValueError as e:
            error = str(e) or "Please enter valid numbers."
        except Exception:
            error = "Something went wrong. Please check your inputs."

    return render_template(
        "index.html",
        prediction=prediction,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
