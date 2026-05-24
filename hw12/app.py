import csv
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

CSV_FILE = "students.csv"
FIELDNAMES = ["id", "first_name", "last_name", "age"]


def init_csv_file():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()


def read_students():
    init_csv_file()

    students = []

    with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["id"] = int(row["id"])
            row["age"] = int(row["age"])
            students.append(row)

    return students


def write_students(students):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()

        for student in students:
            writer.writerow(student)


def get_next_id(students):
    if not students:
        return 1

    max_id = max(student["id"] for student in students)
    return max_id + 1


def validate_fields(data, allowed_fields, required_fields=None):
    if not data:
        return False, "Request body is empty."

    for field in data:
        if field not in allowed_fields:
            return False, f"Unknown field: {field}"

    if required_fields:
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"

    return True, None


def validate_age(age):
    try:
        age = int(age)

        if age <= 0:
            return False, "Age must be greater than 0."

        return True, age

    except ValueError:
        return False, "Age must be a number."


@app.route("/students", methods=["GET"])
def get_all_students():
    students = read_students()
    return jsonify(students), 200


@app.route("/students/<int:student_id>", methods=["GET"])
def get_student_by_id(student_id):
    students = read_students()

    for student in students:
        if student["id"] == student_id:
            return jsonify(student), 200

    return jsonify({"error": "Student with this ID was not found."}), 404


@app.route("/students/surname/<string:last_name>", methods=["GET"])
def get_students_by_last_name(last_name):
    students = read_students()

    found_students = []

    for student in students:
        if student["last_name"].lower() == last_name.lower():
            found_students.append(student)

    if not found_students:
        return jsonify({"error": "Students with this surname were not found."}), 404

    return jsonify(found_students), 200


@app.route("/students", methods=["POST"])
def create_student():
    data = request.get_json()

    allowed_fields = ["first_name", "last_name", "age"]
    required_fields = ["first_name", "last_name", "age"]

    is_valid, error = validate_fields(data, allowed_fields, required_fields)

    if not is_valid:
        return jsonify({"error": error}), 400

    is_age_valid, age_result = validate_age(data["age"])

    if not is_age_valid:
        return jsonify({"error": age_result}), 400

    students = read_students()

    new_student = {
        "id": get_next_id(students),
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "age": age_result
    }

    students.append(new_student)
    write_students(students)

    return jsonify(new_student), 201


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json()

    allowed_fields = ["first_name", "last_name", "age"]
    required_fields = ["first_name", "last_name", "age"]

    is_valid, error = validate_fields(data, allowed_fields, required_fields)

    if not is_valid:
        return jsonify({"error": error}), 400

    is_age_valid, age_result = validate_age(data["age"])

    if not is_age_valid:
        return jsonify({"error": age_result}), 400

    students = read_students()

    for student in students:
        if student["id"] == student_id:
            student["first_name"] = data["first_name"]
            student["last_name"] = data["last_name"]
            student["age"] = age_result

            write_students(students)

            return jsonify(student), 200

    return jsonify({"error": "Student with this ID was not found."}), 404


@app.route("/students/<int:student_id>", methods=["PATCH"])
def update_student_age(student_id):
    data = request.get_json()

    allowed_fields = ["age"]
    required_fields = ["age"]

    is_valid, error = validate_fields(data, allowed_fields, required_fields)

    if not is_valid:
        return jsonify({"error": error}), 400

    is_age_valid, age_result = validate_age(data["age"])

    if not is_age_valid:
        return jsonify({"error": age_result}), 400

    students = read_students()

    for student in students:
        if student["id"] == student_id:
            student["age"] = age_result

            write_students(students)

            return jsonify(student), 200

    return jsonify({"error": "Student with this ID was not found."}), 404


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    students = read_students()

    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            write_students(students)

            return jsonify({
                "message": f"Student with ID {student_id} was successfully deleted."
            }), 200

    return jsonify({"error": "Student with this ID was not found."}), 404


if __name__ == "__main__":
    init_csv_file()
    app.run(debug=True)