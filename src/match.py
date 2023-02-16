import pandas as pd
from Student import Student
from CourseSection import CourseSection

# fix class module errors waaaaa

student_df = pd.DataFrame()
section_df = pd.DataFrame()

def df_get_student(id: int):
    row = student_df.at[id]
    student = Student(id = id, name = row[0], base_score = int(row[1]))
    student.set_section_ranking(row[3].split(" "))
    return student

def df_get_section(id: int):
    row = section_df.at[id]
    section = CourseSection(id = id, course_name = row[0],
                                                capacity = int(row[1]), credits = int(row[2]))
    return section

def df_update_student(student: Student):
    # currently only updates section ranking field because that is the only one that may change
    student_df.iat[student.id, 3] = str(student.section_ranking)
    

def df_update_section(section: CourseSection, df: pd.DataFrame):
    # currently only updates roster, will need to update removed if I end up using it
    roster = []
    for student in section.roster_pq.queue:
        roster.append(student.id)
    section_df.iat[section.id, 4] = str(roster)

def add_student_to_section(student: Student, section: CourseSection):
    student.join_section(section)
    section.enroll(student)
    return student, section

def try_enrolling(student: Student, section: CourseSection):
        if student.credits_enrolled + section.credits > student.credit_limit:
            print(f'student #{student.id} could not enroll in section #{section.id}'
                  +' because they are taking too many credits')
            return student, section
        elif section.is_full():
            if section.score_student(student) > section.student_score_pq[0]:
                removed_student = section.pop_lowest_student() # currently does nothing, try new addition to removed dict?
                return add_student_to_section(student, section)
            else:
                print(f'student #{student.id} could not enroll in section #{section.id}'
                  +' because the section is full of higher priority students')
                return student, section
        else:
            return add_student_to_section(student, section)

def main():
    student_list = []
    student_df = pd.read_csv("../test_data/test_students.csv",  delimiter = ",")
    student_df.set_index("id", inplace = True)
    
    print(student_df)
    
    for index, row in student_df.iterrows():
        new_student = Student(id = index, name = row[0], base_score = int(row[1]))
        student_list.append(new_student)
        
    section_list = []
    section_df = pd.read_csv("../test_data/test_sections.csv")
    section_df.set_index("id", inplace = True)
    
    print(section_df)
    
    for index, row in section_df.iterrows():
        new_section = CourseSection(id = index, course_name = row[0],
                                                capacity = int(row[1]), credits = int(row[2]))
        section_list.append(new_section)
        
    free_students, free_sections = [], []
    
    # populate new free (not at capacity) lists with ids, for more info dataframe can be referenced
        
    for student in student_list:
        free_students.append(student.id)
        print(student)
    for section in section_list:
        free_sections.append(section.id)
        print(section)
        
    for index, row in section_df.iterrows():
        print(index)
        
    test_section = df_get_section(100000)
    print(f'test section:\n{test_section}')
    test_section.enroll(df_get_student(10000000))
    print(f'test section updated:\n{test_section}')
    df_update_section(test_section)
    print(f'dataframe updated:\n {section_df}')
    
    
main()
    