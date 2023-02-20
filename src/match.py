import pandas as pd
from Student import Student
from CourseSection import CourseSection

#student aren't getting section rankings for some reason, also handle the possiblity that they might not have 
# a ranking anyway in the gale shapely method
# something like while they have a next section - if they have space for that section

section_df = pd.DataFrame() # dataframe serves as intemediary between CSV and dict
section_dict = {} # source of truth during program
student_df = pd.DataFrame()
student_dict = {}

def student_dict_to_df():
    pass

def section_dict_to_df():
    pass

def get_df_student(id: int):
    row = student_df.loc[id] # figure out how to make this work next!
    student = Student(id = id, name = row[0], base_score = int(row[1]))
    student.set_section_ranking(row[2].split(" "))
    return student

def get_df_section(id: int):
    print(section_df.index)
    row = section_df.loc[id]
    section = CourseSection(id = id, course_name = row[0],
                                                capacity = int(row[1]), credits = int(row[2]))
    return section

def update_student_df(student: Student):
    # currently only updates section ranking field because that is the only one that may change
    student_df.at[student.id, 3] = str(student.section_ranking)
    
def update_section_df(section: CourseSection):
    # currently only updates roster, will need to update removed if I end up using it
    roster = []
    for student in section.roster_pq.queue:
        roster.append(student.id)
    section_df.at[section.id, 'roster_ids'] = str(roster)[1:-1]

def add_student_to_section(student: Student, section: CourseSection):
    student.join_section(section)
    section.enroll(student)
    return student, section

def try_enrolling(student: Student, section: CourseSection):
        # print("running try enrolling")
        if student.credits_enrolled + section.credits > student.credit_limit: # this is maybe redundant with  new is free method?
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
        
def try_enrolling_next_section(student: Student):
    top_section = section_dict[student.get_top_section_id()]
    student.increment_next_section()
    return try_enrolling(student, top_section)
        
def Gale_Shapley():
    # just needs logic for students kicked out of sections, and handling for students who want lower credits courses
    # but dont have space for more credit courses before them
    free_students = []
    for id in student_dict:
        free_students.append(id)
    while len(free_students) > 0:
        cur_student = student_dict[free_students[-1]]
        while not cur_student.is_finished_proposing():
            if not cur_student.has_credits_to_fill(section_dict[cur_student.get_top_section_id()].credits):
                break
            cur_student_new, proposed_section_new = try_enrolling_next_section(cur_student)
            student_dict[cur_student.id] = cur_student_new
            section_dict[proposed_section_new.id] = proposed_section_new
            cur_student = cur_student_new
        free_students.pop()

def main():
    global student_dict
    global section_dict
    global student_df
    global section_df
    
    student_list = []
    student_df = pd.read_csv("../test_data/test_students.csv",  delimiter = ",")
    student_df.set_index("id", inplace = True)

    print(student_df)

    for index, row in student_df.iterrows():
        new_student = Student(id = index, name = row[0], base_score = int(row[1]))
        new_student.set_section_ranking(row[2].split(" "))
        student_list.append(new_student)
        student_dict[new_student.id] = new_student
        
    section_list = []
    section_df = pd.read_csv("../test_data/test_sections.csv")
    section_df.set_index("id", inplace = True)

    print(section_df)

    for index, row in section_df.iterrows():
        new_section = CourseSection(id = index, course_name = row[0],
                                                capacity = int(row[1]), credits = int(row[2]))
        section_list.append(new_section)
        section_dict[new_section.id] = new_section
        
        
    for key in student_dict:
        print(student_dict[key])
    for key in section_dict:
        print(section_dict[key])
        
    Gale_Shapley()
    
    print("post GS students")

    for key in student_dict:
        print(student_dict[key])
        
    print("post GS sections")
    
    for key in section_dict:
        print(section_dict[key])
        
main()
    