import sys
from pprint import pprint

sys.path.append("src")

import data

from gs import gale_shapley_match
from test_stability import is_weakly_stable
from student import Student

sys.path.append("/..")

sections = data.section_csv_to_dict("CsCoursesSpring24.csv")

student_df = data.student_csv_to_df("Students.csv")
students = {}

for index, row in student_df.iterrows():
    
    # score for student
    base_score = 0
    
    # majors are prioritized over minors, scores are slightly adjusted based on whether they have declared
    major = row[3]
    if major == "major":
        base_score = 1000
    elif major == "intended major":
        base_score = 990
    elif major == "minor":
        base_score = 10
    elif major == "none of the above":
        base_score = 0
        
    taken_courses = row[4]
    taken_courses = taken_courses.split(" ")
    taken_count = len(taken_courses)
    courses_left = 13 - taken_count if major == "major" or major == "intended major" else 5 - taken_count
    
    # scores mainly based on number of courses needed to be "on track" (2 courses left per semester)
    grad_semester = row[5]
    if grad_semester == "Spring 2024":
        courses_needed = courses_left
        base_score += 250 # +2 courses needed for graduating seniors, only juniors who need courses to have 4 per semester will be prioritized over them
    elif grad_semester == "Fall 2024":
        courses_needed = courses_left - 2
        base_score += 40
    elif grad_semester == "Spring 2025":
        courses_needed = courses_left - 4
        base_score += 30
    elif grad_semester == "Fall 2025":
        courses_needed = courses_left - 6
        base_score += 20
    elif grad_semester == "Spring 2026":
        courses_needed = courses_left - 8
        base_score += 10
    
    # students who are ahead will be prioritized the same
    courses_needed = max(courses_needed, 0)
    courses_needed = min(courses_needed, 4)
    base_score += courses_needed * 100
    
    section_limit = max(int(row[19]), 4)
        
    new_student = Student(
        id=row[2], name=row[1], major="NA", base_score=base_score,
    )

    new_student.section_limit = section_limit
    # set section ranking: ADD CRN TO SURVEY

    students[new_student.id] = new_student

gale_shapley_match(students, sections)
for section in sections.values():
    print(section)
print(is_weakly_stable(students, sections))
