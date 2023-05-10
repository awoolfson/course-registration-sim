import pandas as pd
from Student import Student
from CourseSection import CourseSection
import json
import random

student_filepath = "../test_data/test_students_2.csv"
section_filepath = "../test_data/test_sections_2_rogue.csv"

def student_csv_to_df(student_filepath):
    student_df = pd.read_csv(student_filepath,  delimiter = ",")
    student_df.set_index("id", inplace = True)
    return student_df

def student_df_to_dict(student_df):
    student_dict = {}
    for index, row in student_df.iterrows():
        new_student = Student(id = index, name = row[0], base_score = int(row[1]), major = row[2])
        new_student.set_section_ranking(row[3].split(" "))
        student_dict[new_student.id] = new_student
    return student_dict

def student_csv_to_dict(student_filepath):
    student_df = student_csv_to_df(student_filepath)
    student_dict = student_df_to_dict(student_df)
    return student_dict

def section_csv_to_df(section_filepath):
    section_df = pd.read_csv(section_filepath)
    section_df.set_index("id", inplace = True)
    return section_df

def section_df_to_dict(section_df):
    section_dict = {}
    for index, row in section_df.iterrows():
        new_section = CourseSection(id = index, code = row[0],
                                                capacity = int(row[1]), credits = int(row[2]),
                                                dept = row[3], name = row[4], days = row[5].split(" "),
                                                times = row[6].split('+'))
        section_dict[new_section.id] = new_section
    return section_dict

def section_csv_to_dict(section_filepath):
    section_df = section_csv_to_df(section_filepath)
    section_dict = section_df_to_dict(section_df)
    return section_dict

def section_JSON_to_dict(filepath):
    with open (filepath, 'r') as f:
        raw_sections = json.loads(f.read())
    section_dict = {}
    for crn in raw_sections:
        data = raw_sections[crn]
        new_section = CourseSection(id = int(crn), code = data['code'],
                                    capacity = int(data['cap']), credits = 4, #credits = int(data['credits'][0]),
                                    name = data['name'], dept = data['dept'], times = data['time'],
                                    days = data['days'])
        section_dict[int(crn)] = new_section
    return section_dict

def remove_TBAs(section_dict) -> dict:
    for crn in section_dict:
        if section_dict[crn].days == ['TBA'] or section_dict[crn].times == ['TBA']:
            section_dict.pop(crn)

def generate_students_weighted(section_dict, n):
    depts = []
    crns = []
    student_dict = {}
    
    for crn in section_dict:
        crns.append(crn)
        if section_dict[crn].dept not in depts:
            depts.append(section_dict[crn].dept)
            
    for i in range(n):
        id = i
        year = random.randint(1, 5)
        base_score = year * 100
        major = random.choice(depts)
        name = "student" + str(i) + "(" + major + str(year) + ")"
        section_ranking = []
        section_index = random.randrange(0, len(crns))
        crn_options = list(crns)
        for c in range(random.randrange(5, 6)): # gives students 10 picks for courses
            section_id = None
            coin = random.randrange(0, 2)
            if coin == 1:
                maj_dept = []
                for crn in crn_options:
                    if section_dict[crn].dept == major:
                        maj_dept.append(crn)
                if len(maj_dept) > 0:
                    section_id = random.choice(maj_dept)
            if section_id == None:
                section_index = random.randrange(0, len(crn_options))
                section_id = crn_options[section_index]
            
            # if section is not in the same major, the student will have a 50% chance of choosing a new one in major
                            
            crn_options.remove(section_id)
            section_ranking.append(section_id)
        new_student = Student(id = id, name = name, base_score = base_score,
                              major = major)
        new_student.set_section_ranking(section_ranking)
        
        new_student.find_conflicts(section_dict)
        
        student_dict[id] = new_student
    return student_dict