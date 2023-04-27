import pandas as pd
from Student import Student
from CourseSection import CourseSection
import data
import test_stability

"""
TODO
- finish time conflicts implementation
- test stability method update with counter
- nice data
- Design patters for the objects
- add full student scoring function
- implement different generate students method
"""

section_df = pd.DataFrame() # dataframe serves as intemediary between CSV and dict
section_dict = {} # source of truth during program
student_df = pd.DataFrame()
student_dict = {}

def add_student_to_section(student: Student, section: CourseSection):
    student.join_section(section)
    section.enroll(student)
    return student, section

def try_enrolling(student: Student, section: CourseSection):
    
    # checks if a student has enough credits, if course has space or student is better than current enrolled
    # returns updated objects
    
        section.swapped_out = (False, 0) # default to no student swapping
        if student.credits_enrolled + section.credits > student.credit_limit: # this is maybe redundant with  new is free method?
            print(f'student #{student.name} could not enroll in section {section.course_code}: {section.id}'
                  +' because they are taking too many credits\n\n')
            return student, section
        elif section.is_full():
            if section.score_student(student) > section.return_lowest_student().section_score:
                removed_student = section.pop_lowest_student() # currently does nothing, try new addition to removed dict?
                section.swapped_out = (True, removed_student.id)
                print(f'student {removed_student.name} swapped out for {student.name}\n in section: {section.course_code}: {section.id}\n\n')
                return add_student_to_section(student, section)
            else:
                print(f'student #{student.name} could not enroll in section {section.course_code}: {section.id}'
                  +' because the section is full of higher priority students\n\n')
                return student, section
        else:
            return add_student_to_section(student, section)
        
def try_enrolling_top_section(student: Student):
    
    # handles student top section pointer and calls try_enrolling
    
    proposed_section = section_dict[student.get_top_section_id()]
    print(f"trying to enroll {student.name} in {proposed_section.course_name}\n\n")
    student.add_proposal(proposed_section.id)
    return try_enrolling(student, proposed_section)
        
def Gale_Shapley():
    
    print("\nstarting Gale-Shapley\n")
    
    # initialize and populate free students list
    
    free_students = []
    for id in student_dict:
        free_students.append(id)
        
    # look at last student in free list
    
    while len(free_students) > 0:
        to_pop = True # this determines if a student has been swapped out and a pop on the free student list is not needed
        cur_student = student_dict[free_students[-1]]
        
        # while student has more sections to propose to
        
        while cur_student.can_propose():
            
            print(f"proposing student: {cur_student.name}\n\n")
            
            # try enrolling student in favorite section
            
            updated_agents = try_enrolling_top_section(cur_student)
            cur_student_new, proposed_section_new = updated_agents[0], updated_agents[1]
            
            # update dictionaries with returned student and section objects
            
            student_dict[cur_student.id] = cur_student_new
            section_dict[proposed_section_new.id] = proposed_section_new
            
            print(f"{cur_student.name} after proposal:\n\n {cur_student_new}\n\n {proposed_section_new.course_code}: "
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
    
    # section_dict = data.section_JSON_to_dict("../scraping/classes.json")
    # student_dict = data.generate_students(section_dict, 200)
        
    print("\n\nall students initialized:\n\n")
        
    for key in student_dict:
        print(student_dict[key])
        student_dict[key].find_conflicts(section_dict)
        print(student_dict[key].conflicts_dict)
        
    print("all sections initialized\n\n")
    
    for key in section_dict:
        print(section_dict[key])
        
    Gale_Shapley()
    
    print("""
          post GS students
        ------------------------\n
          """)

    for key in student_dict:
        print(student_dict[key])
        
    print("""
          post GS sections
        ------------------------\n
          """)
    
    for key in section_dict:
        print(section_dict[key])
        
    # student_dict[40000000].section_ranking[0] = 800000
    # used for testing instability
        
    is_pairwise_stable = test_stability.is_pairwise_stable(student_dict=student_dict, section_dict=section_dict)
    print(f'\n\nThis matching is pairwise stable? {is_pairwise_stable}')
         
main()
    