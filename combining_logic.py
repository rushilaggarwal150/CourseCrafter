import json

# Open and read the course data file
with open("courses.json", "r") as course_file:
    courses_data = json.load(course_file)

# Open the grades_by_course.txt file and read each line
with open("grades_by_course.txt", "r") as grade_file:
    grade_data = [json.loads(line.strip()) for line in grade_file]

# Create a dictionary for easy lookup based on course number
grade_dict = {str(entry["course_number"]): entry["text"] for entry in grade_data}

# Open the catalog.txt file for writing
with open("Data_files/Catalog.txt", "w") as catalog_file:
    # Iterate through courses and write to the catalog file
    for course in courses_data:
        course_number = str(course["Course Number"])
        if course_number in grade_dict:
            additional_text = grade_dict[course_number]
            catalog_file.write(
                f"Course Title: CSCE {course_number}, Description: {course['Description']}\n{additional_text}\n\n"
            )
        else:
            catalog_file.write(
                f"Course Title: CSCE {course_number}, Description: {course['Description']}\n\n"
            )

print("Catalog file created successfully.")
