"""
Auden Woolfson, 2023
This file contains the code responsible for 1. parsing the student and section data from CSV files,
2. scoring students according to their answers to the survey questions, and 3. running the Gale-Shapley style
algorithm to match students to sections. 4. (in progress) saving the matching to a CSV file

Students are scored based on a number of factors. The first factor is whether thet are a major, 
intended major, minor, or "none of the above". Majors will have first priority with 1000 as their starting base
score, and intended majors will follow closely behind at 990. Minors and and "none of the above" students will have 
a similar relationship, with starting base scores of 10 and 0 respectively. The rationale behind this is that
majors will always be prioritized over minors unless the minor is in dire need of courses.

The second factor students scores are based on is their graduation semester and the number of remaining courses
they need to recieve the major/minor (0 if they are not on the major or minor track). They are given an additional 100 points
for each course they need to take in order to reach the "on track" number of courses (2 per semester). This is to ensure
no student gets too far behind. That being said, in order to prevent seniors who absolutely need their remaining courses from
being blocked by juniors or sophomores who just need to catch up to a more manageable number of courses, graduating
seniors are given +1200 to their base score. This dictates the ultimate priority of the scoring function, which is seniors
who need to finish. It also does allow for cases in which senior minors who need courses can be prioritized over 
majors who need courses less urgently. This is intentional.

Students are also given an additional 50 points if they are graduating in Spring 2024, 40 points if they are graduating
in Fall 2025, 30 points if they are graduating in Spring 2025, 20 points if they are graduating in Fall 2025, and 10 points
if they are graduating in Spring 2026. These small sums act as tie breakers between students with otherwise identical scores.

Note that the courses needed variable is bounded between 0 and 4. This is so students who are ahead of schedule
(negative) or on schedule (0) will be prioritized the same. Students will not be punished for being ahead of schedule.
It also prevents students who are very far behind from being prioritized over students who are only slightly behind.
"""

import sys
from pprint import pprint
import re
import pandas as pd

sys.path.append("../src")

from data import section_csv_to_dict

from gs import gale_shapley_match
from test_stability import is_weakly_stable
from student import Student

sections = section_csv_to_dict("cs_courses_spring24.csv")

response_df =  pd.read_csv("google_form_students.csv")
students = {}

for index, row in response_df.iterrows():
    
    # score for student
    base_score = 0
    
    # majors are prioritized over minors, scores are slightly adjusted based on whether they have declared
    taken_courses = row[4]
    taken_courses = taken_courses.split(",")
    taken_count = len(taken_courses)
    major = row[3]
    
    if major == "major":
        base_score = 1000
        courses_left = 13 - taken_count
    elif major == "intended major":
        base_score = 990
        courses_left = 13 - taken_count
    elif major == "minor":
        base_score = 10
        courses_left = 5 - taken_count
    else: # none of the above
        base_score = 0
        courses_left = 0
    
    # scores mainly based on number of courses needed to be "on track" (2 courses left per semester)
    grad_semester = row[5]
    if grad_semester == "Spring 2024":
        courses_needed = courses_left
        base_score += 650 if courses_needed == 0 else 50
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
    # courses_needed = min(courses_needed, 4)
    base_score += courses_needed * 100
    
    desired = min(int(row[20]), courses_needed)
    section_limit = min(desired, 4)
    
    crns = {
        "212-1": 10324,
        "212-2": 10325,
        "219-1": 10746,
        "302-1": 10326,
        "303-1": 10327,
        "304-1": 10328,
        "310-1": 10330,
        "313-1": 10331,
        "315-1": 10332,
        "428-1": 10813,
        "496-1": 10334,
        "496-2": 10335,
        } # include course label to CRN matching here
    
    pattern = "([0-9]{3}-[0-9]{1})"
    ranking = []
    for i in range(6, 20):
        number = re.match(pattern, row[i])
        number = number.group(1)
        if crn := crns.get(number, None):
            ranking.append(crn)
        
    new_student = Student(
        id=row[2], name=row[1], major="NA", base_score=base_score,
    )

    new_student.set_section_ranking(ranking)
    new_student.section_limit = section_limit
    # set section ranking: ADD CRN TO SURVEY

    students[new_student.id] = new_student

gale_shapley_match(students, sections)
for section in sections.values():
    print(section)
for student in students.values():
    print(student)
print(is_weakly_stable(students, sections))
