import requests
import json

BASE_URL = "http://127.0.0.1:5000"


def save_and_print(file, title, response):
    result = {
        "status_code": response.status_code,
        "response": response.json()
    }

    text = f"\n===== {title} =====\n"
    text += json.dumps(result, indent=4, ensure_ascii=False)

    print(text)

    file.write(text)
    file.write("\n")


with open("results.txt", mode="w", encoding="utf-8") as file:

    response = requests.get(f"{BASE_URL}/students")
    save_and_print(file, "1. GET all students", response)

    student_1 = {
        "first_name": "John",
        "last_name": "Smith",
        "age": 20
    }

    student_2 = {
        "first_name": "Anna",
        "last_name": "Brown",
        "age": 22
    }

    student_3 = {
        "first_name": "Tom",
        "last_name": "Wilson",
        "age": 24
    }

    response = requests.post(f"{BASE_URL}/students", json=student_1)
    created_student_1 = response.json()
    save_and_print(file, "2. POST create first student", response)

    response = requests.post(f"{BASE_URL}/students", json=student_2)
    created_student_2 = response.json()
    save_and_print(file, "3. POST create second student", response)

    response = requests.post(f"{BASE_URL}/students", json=student_3)
    created_student_3 = response.json()
    save_and_print(file, "4. POST create third student", response)

    response = requests.get(f"{BASE_URL}/students")
    save_and_print(file, "5. GET all students after POST", response)

    second_student_id = created_student_2["id"]

    response = requests.patch(
        f"{BASE_URL}/students/{second_student_id}",
        json={"age": 23}
    )
    save_and_print(file, "6. PATCH update second student age", response)

    response = requests.get(f"{BASE_URL}/students/{second_student_id}")
    save_and_print(file, "7. GET second student by ID", response)

    third_student_id = created_student_3["id"]

    updated_third_student = {
        "first_name": "Robert",
        "last_name": "Johnson",
        "age": 25
    }

    response = requests.put(
        f"{BASE_URL}/students/{third_student_id}",
        json=updated_third_student
    )
    save_and_print(file, "8. PUT update third student", response)

    response = requests.get(f"{BASE_URL}/students/{third_student_id}")
    save_and_print(file, "9. GET third student by ID", response)

    response = requests.get(f"{BASE_URL}/students")
    save_and_print(file, "10. GET all students before DELETE", response)

    first_student_id = created_student_1["id"]

    response = requests.delete(f"{BASE_URL}/students/{first_student_id}")
    save_and_print(file, "11. DELETE first student", response)

    response = requests.get(f"{BASE_URL}/students")
    save_and_print(file, "12. GET all students after DELETE", response)