from Student import Student
from CourseSection import CourseSection

def is_pairwise_stable(student_dict, section_dict):
    for key in student_dict:
        cur_student = student_dict[key]

        cur_student_remaining_schedule = cur_student.schedule # used to check if iteration has passed the lowest ranked course in schedule
        
        for index, section_id in enumerate(cur_student.section_ranking):
            cur_section = section_dict[section_id]
            if not section_id in cur_student.schedule:
                if not cur_section.is_full():
                    return False
                elif cur_section.return_lowest_student().section_score < cur_section.score_student(cur_student):
                    return False
            else:
                cur_student_remaining_schedule.remove(section_id)
                if len(cur_student_remaining_schedule) == 0:
                    break
    return True