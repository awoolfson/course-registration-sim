import pandas as pd
from Student import Student
from CourseSection import CourseSection
import json
import random

student_filepath = "../test_data/test_students_2.csv"
section_filepath = "../test_data/test_sections_2.csv"

def student_csv_to_df():
    student_df = pd.read_csv(student_filepath,  delimiter = ",")
    student_df.set_index("id", inplace = True)
    print(student_df)
    return student_df

def student_df_to_dict(student_df):
    student_dict = {}
    for index, row in student_df.iterrows():
        new_student = Student(id = index, name = row[0], base_score = int(row[1]), major = row[2])
        new_student.set_section_ranking(row[3].split(" "))
        student_dict[new_student.id] = new_student
    return student_dict

def section_csv_to_df():
    section_df = pd.read_csv(section_filepath)
    section_df.set_index("id", inplace = True)

    print(section_df)
    return section_df

def section_df_to_dict(section_df):
    section_dict = {}
    for index, row in section_df.iterrows():
        new_section = CourseSection(id = index, code = row[0],
                                                capacity = int(row[1]), credits = int(row[2]),
                                                dept = row[3], name = row[4], days = row[5].split(" "),
                                                times = row[6].split('+')) #add time and days to this
        section_dict[new_section.id] = new_section
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
        
def generate_students(section_dict, n):
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
        name = "student" + str(i) + "(" + str(year) + ")"
        base_score = year * 100
        major = random.choice(depts)
        section_ranking = []
        used_indices = []
        section_index = random.randrange(0, len(crns))
        
        for c in range(10): # gives students 10 picks for courses
            while section_index in used_indices:
                section_index = random.randrange(0, len(crns))
            used_indices.append(section_index)
            section_id = crns[section_index]
            section_ranking.append(section_id)
        new_student = Student(id = id, name = name, base_score = base_score,
                              major = major)
        new_student.set_section_ranking(section_ranking)
        
        new_student.find_conflicts(section_dict)
        
        student_dict[id] = new_student
    return student_dict