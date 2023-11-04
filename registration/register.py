"""
Auden Woolfson, 2023
TODO:
- prereqs checking and blocking
"""

import sys
from pprint import pprint
import re
import pandas as pd

sys.path.append("../src")

from data_methods import section_csv_to_dict

from gs import gale_shapley_match
from test_stability import check_stability
from student import Student

def main():
    sections = section_csv_to_dict("cs_courses_spring24.csv")

    total_seats = sum(map(lambda x: x.capacity, sections.values()))
    remaining_seats = total_seats

    response_df =  pd.read_csv("google_form_students.csv")
    students = {}

    for index, row in response_df.iterrows():
        
        base_score = 0
        
        taken_courses = row[4]
        taken_courses = taken_courses.split(",")
        taken_count = len(taken_courses)
        status = row[3]
        
        # base score heavily based on major status
        if status == "declared CS major":
            base_score = 3000
            courses_left = 12 - taken_count
            major = "major"
        elif status == "intended CS major":
            base_score = 2000
            courses_left = 12 - taken_count
            major = "intended"
        elif status == "CS minor":
            base_score = 1000
            courses_left = 5 - taken_count
            major = "minor"
        else:
            base_score = 0
            courses_left = 0
            major = "none"
        
        # modifiers to base score applied based on seniority
        grad_semester = row[5]
        if grad_semester == "Spring 2024":
            courses_needed_soft = courses_left
            courses_needed_hard = courses_left
            base_score += 80
        elif grad_semester == "Fall 2024":
            courses_needed_soft = courses_left - 2
            courses_needed_hard = courses_left - 4
            base_score += 70
        elif grad_semester == "Spring 2025":
            courses_needed_soft = courses_left - 4
            courses_needed_hard = courses_left - 8
            base_score += 60
        elif grad_semester == "Fall 2025":
            courses_needed_soft = courses_left - 6
            courses_needed_hard = courses_left - 12
            base_score += 50
        elif grad_semester == "Spring 2026":
            courses_needed_soft = courses_left - 8
            courses_needed_hard = courses_left - 16
            base_score += 40
        elif grad_semester == "Fall 2026":
            courses_needed_soft = courses_left - 10
            courses_needed_hard = courses_left - 20
            base_score += 30
        elif grad_semester == "Spring 2027":
            courses_needed_soft = courses_left - 12
            courses_needed_hard = courses_left - 24
            base_score += 20
        elif grad_semester == "Fall 2027":
            courses_needed_soft = courses_left - 14
            courses_needed_hard = courses_left - 28
            base_score += 10
        
        courses_needed_soft = max(courses_needed_soft, 0)
        courses_needed_hard = max(courses_needed_hard, 0)
        
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
            "214-1": 10840
            }
        
        pattern = "([0-9]{3})"
        taken = set()
        taken_entry = row[4]
        taken_entry = taken_entry.split(",")
        for entry in taken_entry:
            number = re.findall(pattern, entry)[0]
            taken.add(number)
        
        pattern = "([0-9]{3}-[0-9]{1})"
        ranking = []
        for i in list(range(6, 20)) + [25]:
            if type(row[i]) == str:
                number = re.match(pattern, row[i])
                number = number.group(1)
                if number[:3] not in taken or number[:3] in ["495", "496"]:
                    if crn := crns.get(number, None):
                        ranking.append(crn)
                else:
                    print(f"{row[1]} has selected {number} as taken")
            
        # tier 1: majors needs
        section_limit = min(courses_needed_soft, row[20], 4, len(ranking)) if major == "major" else 0
        remaining_seats -= section_limit
        
        new_student = Student(
            id = "00" + str(row[2]), name=row[1], major=major, base_score=base_score,
            **{
                "courses_needed_soft": courses_needed_soft,
                "courses_needed_hard": courses_needed_hard,
                "courses_desired": row[20],
                "grad_semester": grad_semester,
                "max_seats": min(4, len(ranking), row[20]),
                "courses_taken": taken,
                }
        )

        new_student.set_section_ranking(ranking)
        new_student.section_limit = section_limit

        new_student.find_conflicts(sections)

        if new_student.name != "awoolfson@conncoll.edu":
            students[new_student.id] = new_student

    prev_remaining_seats = remaining_seats
    iteration = 0
    while remaining_seats > 0:
        
        # tier 2: majors who haven't gotten any courses
        for student in students.values():
            if student.section_limit == 0 and student.major == "major" and \
            student.info["max_seats"] > student.section_limit and \
            remaining_seats > 0 and \
            student.section_limit < len(student.section_ranking):
                student.section_limit += 1
                remaining_seats -= 1
        
        # tier 3: minors who need one last course
        for student in students.values():
            if student.major == "minor" and \
            student.info["grad_semester"] == "Spring 2024" and \
            student.info["max_seats"] > student.section_limit and \
            student.section_limit == student.info["courses_needed_hard"] - 1 and \
            remaining_seats > 0:
                student.section_limit += 1
                remaining_seats -= 1

        # tier 4: graduating majors who want an extra course
        for student in students.values():
            if student.info["grad_semester"] == "Spring 2024" and \
            student.info["max_seats"] > student.section_limit and \
            student.major == "major" and \
            remaining_seats > 0:
                student.section_limit += 1
                remaining_seats -= 1
                
        # tier 5: intended majors needs
        for student in students.values():
            if student.major == "intended":
                while student.info["max_seats"] > student.section_limit and remaining_seats > 0:
                    student.section_limit += 1
                    remaining_seats -= 1
                
        # tier 6: non senior majors who want an extra course
        for student in students.values():
            if student.info["grad_semester"] != "Spring 2024" and \
            student.major == "major" and \
            student.info["max_seats"] > student.section_limit and \
            remaining_seats > 0:
                student.section_limit += 1
                remaining_seats -= 1
                
        # tier 7: all minors who want an extra course
        for student in students.values():
            if student.major == "minor" and \
            student.info["max_seats"] > student.section_limit and \
            remaining_seats > 0:
                student.section_limit += 1
                remaining_seats -= 1
                
        # tier 8: other
        for student in students.values():
            if student.section_limit <= iteration and \
            student.info["max_seats"] > student.section_limit and \
            remaining_seats > 0:
                student.section_limit += 1
                remaining_seats -= 1
                
        if prev_remaining_seats == remaining_seats:
            break
        prev_remaining_seats = remaining_seats
        iteration += 1
        
    # give those minors with one more course the needed boost
    for student in students.values():
        if student.major == "minor" and \
        student.info["grad_semester"] == "Spring 2024" and \
        student.info["courses_needed_hard"] == 1:
            student.base_score += 1000
                
    gale_shapley_match(students, sections)
    
    for section in sections.values():
        if len(section.roster_pq) < section.capacity:
            print(f"\n{section.course_name} has {section.capacity - len(section.roster_pq)} empty seats")
    
    print(check_stability(students, sections))

    total_desired_seats = sum(map(lambda x: x.info["courses_desired"], students.values()))
    total_allocated_seats = sum(map(lambda x: x.section_limit, students.values()))
    total_filled_seats = sum(map(lambda x: len(x.roster_pq), sections.values()))
    total_seats = sum(map(lambda x: x.capacity, sections.values()))

    print(f"total desired seats: {total_desired_seats}")
    print(f"total allocated seats: {total_allocated_seats}")
    print(f"total filled seats: {total_filled_seats}")
    print(f"total seats: {total_seats}")

    ids = list(students.keys())
    students_output = list(students.values())
    
    students_output = list(map(
        lambda x: [
            x.name,
            x.info['grad_semester'],
            x.major,
            x.info['courses_desired'],
            x.info['courses_needed_soft'],
            x.info['courses_needed_hard'],
            x.section_limit,
            len(x.enrolled_in),
            x.enrolled_in,
            list(map(
                lambda y: sections[y].course_code + ", " + sections[y].course_name,
                x.enrolled_in
            ))],
        students_output
        ))
    
    students_output = pd.DataFrame(
        students_output, index=ids, columns=[
            "name",
            "grad_semester",
            "major_status",
            "num_desired",
            "num_needed_soft",
            "num_needed_hard",
            "num_allocated",
            "num_given",
            "enrolled_in",
            "enrolled_in_names"
            ])
    
    students_output.to_csv("output_students.csv")

    crns = list(sections.keys())
    sections_output = list(sections.values())
    sections_output = list(map(
        lambda x: [
            x.course_name, 
            len(x.roster_pq), 
            list(map(lambda y: (y[1], students[y[1]].name), x.roster_pq))
            ], 
        sections_output
        ))
    
    sections_output = pd.DataFrame(sections_output, index=crns, columns=["course_name", "num_enrolled", "roster"])
    sections_output.to_csv("output_sections.csv")
    
    for section in sections.values():
        roster = list(map(lambda x: x[1], section.roster_pq))
        filepath = "individual_sections/" + section.course_code + ".csv"
        section_output = students_output[students_output.index.isin(roster)]
        section_output.to_csv(filepath)
    
if __name__ == "__main__":
    main()
