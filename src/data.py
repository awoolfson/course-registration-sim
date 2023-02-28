import pandas as pd
from Student import Student
from CourseSection import CourseSection

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
        new_student = Student(id = index, name = row[0], base_score = int(row[1]))
        new_student.set_section_ranking(row[2].split(" "))
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
        new_section = CourseSection(id = index, course_name = row[0],
                                                capacity = int(row[1]), credits = int(row[2]))
        section_dict[new_section.id] = new_section
    return section_dict