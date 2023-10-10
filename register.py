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
    
    base_score = 0
    major = row[3]
    if major == "major":
        base_score = 100
    elif major == "intended major":
        base_score = 90
    elif major == "minor":
        base_score = 10
    elif major == "none of the above":
        base_score = 0
    
    grad_semester = row[4]
    if grad_semester == "Spring 2024":
        base_score += 50
    elif grad_semester == "Fall 2025":
        base_score += 40
    elif grad_semester == "Spring 2025":
        base_score += 30
    elif grad_semester == "Fall 2026":
        base_score += 20
    elif grad_semester == "Spring 2026":
        base_score += 10
        
    new_student = Student(
        id=row[2], name=row[1], major="NA", base_score=base_score,
    )
    new_student.set_section_ranking(row[3].split(" "))
    students[new_student.id] = new_student

gale_shapley_match(students, sections)
for section in sections.values():
    print(section)
print(is_weakly_stable(students, sections))
