import random

from section import CourseSection
from student import Student

seed = random.randrange(0, 1000)

def gale_shapley_match(student_dict: dict, 
                 section_dict: dict, 
                 shuffle: bool = False,
                 seed: int = seed) -> (dict, dict):

    # initialize and populate free students list
    free_students = []
    for id in student_dict:
        free_students.append(id)
        
    if shuffle:
        random.seed(seed)
        random.shuffle(free_students)

    # look at last student in free list
    while len(free_students) > 0:
        to_pop = True  # this determines if a student has been swapped out or a pop on the free student list is not needed
        cur_student = student_dict[free_students[-1]]

        # while student has more sections to propose to
        while cur_student.can_propose():

            # try enrolling student in favorite section
            proposed_section = section_dict[cur_student.get_top_section_id()]
            cur_student.add_proposal(proposed_section.id)

            if not proposed_section.is_full():
                add_student_to_section(cur_student, proposed_section)
            elif (
                    proposed_section.score_student(cur_student)
                    > proposed_section.get_lowest_student()[0]
                ):
                    removed_student_id = proposed_section.pop_lowest_student()[1]
                    removed_student = student_dict[removed_student_id]
                    to_pop = False
                    add_student_to_section(cur_student, proposed_section)

            # if a student in the section has been replaced
            if to_pop == False:
                removed_student.leave_section(proposed_section)
                free_students.append(removed_student.id)
                break

        if to_pop:
            free_students.pop()

    return (student_dict, section_dict)


def add_student_to_section(
    student: Student, section: CourseSection
) -> (Student, CourseSection):
    student.join_section(section)
    section.enroll(student)
