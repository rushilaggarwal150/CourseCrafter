import json

# Open the file and read each line
with open("Data_files/Grade.txt", "r") as file:
    # Split each line by commas and then into key-value pairs
    data = [line.strip().split(',') for line in file]

    # Create a dictionary to store aggregated data based on course number
    course_dict = {}
    for line in data:
        line_dict = {}
        for pair in line:
            key, value = pair.split(':')
            key = key.strip()
            value = value.strip()

            # Convert numeric values to integers
            if key in ["Course Number", "A's", "B's", "C's", "D's", "E's", "F's", "Q's", "GPA"]:
                value = float(value) if key == "GPA" else int(value)
            
            line_dict[key] = value

        # Assuming Course Number is unique, use it as the key in the course_dict
        if 'Course Number' in line_dict:
            course_number = line_dict['Course Number']
            if course_number not in course_dict:
                course_dict[course_number] = {'A_total': 0, 'B_total': 0, 'C_total': 0, 'D_total': 0, 'E_total': 0, 'F_total': 0, 'Q_total': 0, 'total_students': 0, 'professors': set(), 'count': 0, 'GPA_total': 0}

            # Aggregate values for each course
            course_dict[course_number]['A_total'] += line_dict["A's"]
            course_dict[course_number]['B_total'] += line_dict["B's"]
            course_dict[course_number]['C_total'] += line_dict["C's"]
            course_dict[course_number]['D_total'] += line_dict["D's"]
            course_dict[course_number]['E_total'] += line_dict["E's"]
            course_dict[course_number]['F_total'] += line_dict["F's"]
            course_dict[course_number]['Q_total'] += line_dict["Q's"]
            course_dict[course_number]['total_students'] += line_dict["A's"] + line_dict["B's"] + line_dict["C's"] + line_dict["D's"] + line_dict["E's"] + line_dict["F's"] + line_dict["Q's"]
            course_dict[course_number]['professors'].add(line_dict['Professor'])
            course_dict[course_number]['GPA_total'] += line_dict['GPA']
            course_dict[course_number]['count'] += 1

# Write the results to the grades_by_course.txt file
with open("grades_by_course.txt", "w") as output_file:
    for course_number, course_data in course_dict.items():
        professors_text = ', '.join(course_data['professors'])
        avg_gpa = round(course_data['GPA_total'] / course_data['count'], 2)
        percent_a = round((course_data['A_total'] / course_data['total_students']) * 100, 2)
        percent_fq = round((course_data['F_total'] + course_data['Q_total']) / course_data['total_students'] * 100, 2)

        output_data = {
            'course_number': course_number,
            'text': f"Is taught by {professors_text}. The average GPA is {avg_gpa}. On average, {percent_a}% of students get an A, and {percent_fq}% get an F or Q."
        }

        output_file.write(json.dumps(output_data) + '\n')
