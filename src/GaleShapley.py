from Student import Student
from CourseSection import CourseSection
import data
import test_stability

def Gale_Shapley(student_dict, section_dict):
    
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
            
            # try enrolling student in favorite section
            print(f"proposing student: {cur_student.name}\n\n")
            
            proposed_section = section_dict[cur_student.get_top_section_id()]
            cur_student.add_proposal(proposed_section.id)
            
            if not proposed_section.is_full():
                new_agents = add_student_to_section(cur_student, proposed_section)
                cur_student, proposed_section = new_agents[0], new_agents[1]
                print(f"student {cur_student.name} enrolled in {proposed_section.course_name}\n\n")
            else:
                if proposed_section.score_student(cur_student) > proposed_section.return_lowest_student().section_score:
                    removed_student = proposed_section.pop_lowest_student()
                    to_pop = False
                    print(f'student {removed_student.name} swapped out for {cur_student.name}\n in section: \
                        {proposed_section.course_code}: {proposed_section.id}\n\n')
                    new_agents = add_student_to_section(cur_student, proposed_section)
                    cur_student, proposed_section = new_agents[0], new_agents[1]
            
            # update dictionaries with returned student and section objects
            student_dict[cur_student.id] = cur_student
            section_dict[proposed_section.id] = proposed_section
            
            print(f"{cur_student.name} after proposal:\n\n {cur_student}\n\n {proposed_section.course_code}: "
                  + f"{proposed_section.id} after proposal: \n\n {proposed_section}\n\n")
            
            # if a student in the section has been replaced
            if to_pop == False:
                removed_student.leave_section(proposed_section)
                student_dict[removed_student.id] = removed_student
                free_students.append(removed_student.id) # it should be fine anyway if this is duplicate?
                break
            
            # update the student object for the loop
        if to_pop:
            free_students.pop()
            
    return (student_dict, section_dict)
        

def add_student_to_section(student: Student, section: CourseSection):
    student.join_section(section)
    section.enroll(student)
    return student, section

def main():
    if __name__ == "__main__":
        student_dict = data.student_csv_to_dict("../test_data/test_students_2.csv")
        section_dict = data.section_csv_to_dict("../test_data/test_sections_2_rogue.csv")
        student_dict, section_dict = Gale_Shapley(student_dict, section_dict)
        is_stable = test_stability.is_pairwise_stable(student_dict, section_dict)
        if is_stable:
            print("Gale-Shapley is pairwise stable")
        else:
            print("Gale-Shapley is not pairwise stable")
main()
        