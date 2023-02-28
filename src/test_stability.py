from Student import Student
from CourseSection import CourseSection

def is_pairwise_stable(student_dict, section_dict):
    
    # to be tested
    
    for key in student_dict:
        cur_student = student_dict[key]

        cur_student_remaining_schedule = cur_student.schedule # used to check if iteration has passed the lowest ranked course in schedule
        
        for index, section_id in enumerate(cur_student.section_ranking):
            
            if not section_id in cur_student.schedule:
                if not section_dict[section_id].is_full():
                    return False
                else:
                    # ok this is very ugly, fix this and make a variable for cur_section
                    if section_dict[section_id].return_lowest_student().section_score < section_dict[section_id].score_student(cur_student):
                        return False
            else:
                cur_student_remaining_schedule.remove(section_id)
                if len(cur_student_remaining_schedule) == 0:
                    continue # move on to next student if all prefered sections have been examined
        return True