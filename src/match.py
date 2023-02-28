import pandas as pd
from Student import Student
from CourseSection import CourseSection
import data
import test_stability

"""
TODO
- random test input generation file
- seperate testing file, (and data i/o file)?
- make sure test stability works
- create a refresh preferences method for students that puts the courses that fit into credits on top, 
  will eventually handle backups etc
- account for credits issue
- test for efficiency / calculate time complexity
"""

section_df = pd.DataFrame() # dataframe serves as intemediary between CSV and dict
section_dict = {} # source of truth during program
student_df = pd.DataFrame()
student_dict = {}

def student_dict_to_df():
    for key in student_dict:
        update_student_df(student_dict[key])

def section_dict_to_df():
    for key in section_dict:
        update_section_df(section_dict[key])

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
    # currently only updates section ranking and schedule
    student_df.at[student.id, 3] = str(student.section_ranking)
    student_df.at[student.id, 4] = str(student.schedule)
    
def update_section_df(section: CourseSection):
    # currently only updates roster, will need to update removed if I end up using it
    roster = []
    for student in section.roster_pq:
        roster.append(student.id)
    section_df.at[section.id, 'roster_ids'] = str(roster)[1:-1]

def add_student_to_section(student: Student, section: CourseSection):
    student.join_section(section)
    section.enroll(student)
    return student, section

def try_enrolling(student: Student, section: CourseSection):
    
    # checks if a student has enough credits, if course has space or student is better than current enrolled
    # returns updated objects
    
        section.swapped_out = (False, 0) # default to no student swapping
        if student.credits_enrolled + section.credits > student.credit_limit: # this is maybe redundant with  new is free method?
            print(f'student #{student.name} could not enroll in section {section.course_name}: {section.id}'
                  +' because they are taking too many credits\n\n')
            return student, section
        elif section.is_full():
            if section.score_student(student) > section.return_lowest_student().section_score:
                removed_student = section.pop_lowest_student() # currently does nothing, try new addition to removed dict?
                section.swapped_out = (True, removed_student.id)
                print(f'student {removed_student.name} swapped out for {student.name}\n in section: {section.course_name}: {section.id}\n\n')
                return add_student_to_section(student, section)
            else:
                print(f'student #{student.name} could not enroll in section {section.course_name}: {section.id}'
                  +' because the section is full of higher priority students\n\n')
                return student, section
        else:
            return add_student_to_section(student, section)
        
def try_enrolling_next_section(student: Student):
    
    # handles student top section pointer and calls try_enrolling
    
    proposed_section = section_dict[student.get_top_section_id()]
    print(f"trying to enroll {student.name} in {proposed_section.course_name}\n\n")
    student.increment_next_section()
    return try_enrolling(student, proposed_section)
        
def Gale_Shapley():
    
    # initialize and populate free students list
    
    free_students = []
    for id in student_dict:
        free_students.append(id)
        
    # look at last student in free list
    
    while len(free_students) > 0:
        to_pop = True # this determines if a student has been swapped out and a pop on the free student list is not needed
        cur_student = student_dict[free_students[-1]]
        
        # while student has more sections to propose to
        
        while not cur_student.is_finished_proposing():
            
            print(f"proposing student: {cur_student.name}\n\n")
            
            # if they have no more credits they can fulfill
            
            if not cur_student.has_credits_to_fill(section_dict[cur_student.get_top_section_id()].credits):
                print(f"{cur_student.name} has reached their credit limit\n\n")
                break
            
            # try enrolling student in favorite section
            
            updated_agents = try_enrolling_next_section(cur_student)
            cur_student_new, proposed_section_new = updated_agents[0], updated_agents[1]
            
            # update dictionaries with returned student and section objects
            
            student_dict[cur_student.id] = cur_student_new
            section_dict[proposed_section_new.id] = proposed_section_new
            
            print(f"{cur_student.name} after proposal:\n\n {cur_student_new}\n\n {proposed_section_new.course_name}: "
                  + f"{proposed_section_new.id} after proposal: \n\n {proposed_section_new}\n\n")
            
            # if a student in the section has been replaced
            
            if proposed_section_new.swapped_out[0] == True:
                to_pop = False
                swapped_student = student_dict[proposed_section_new.swapped_out[1]]
                swapped_student.leave_section(proposed_section_new)
                student_dict[swapped_student.id] = swapped_student
                free_students.append(swapped_student.id) # it should be fine anyway if this is duplicate?
                cur_student = cur_student_new
                break # break so the swapped student can start proposing
            
            # update the student object for the loop
        if to_pop:
            free_students.pop()
            
        print(free_students)

def main():
    global student_dict
    global section_dict
    global student_df
    global section_df
    
    student_df = data.student_csv_to_df()
    student_dict = data.student_df_to_dict(student_df)
        
    section_df = data.section_csv_to_df()
    section_dict = data.section_df_to_dict(section_df)
        
    print("\n\nall students initialized:\n\n")
        
    for key in student_dict:
        print(student_dict[key])
        
    print("all sections initialized\n\n")
    
    for key in section_dict:
        print(section_dict[key])
        
    Gale_Shapley()
    
    print("""post GS students
        ------------------------\n\n
          """)

    for key in student_dict:
        print(student_dict[key])
        
    print("""post GS sections
        ------------------------\n\n
          """)
    
    for key in section_dict:
        print(section_dict[key])
        
main()
    